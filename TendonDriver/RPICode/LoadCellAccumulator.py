from genericHelperFunctions import *
import serial
import pdb
import threading
import io
import sys
import time
from serial.tools import list_ports
import numpy as np

"""
@title LoadCellCalibrationProfile
@description Pure data class that contains the information relevant to the load cell accumulators on a per-unit basis
"""
class LoadCellCalibrationProfile(object):
    """Intercept is set to always be at zero; the offset brings it to zero"""

    def __init__(self, slope, offset):
        super(LoadCellCalibrationProfile, self).__init__()
        self.slope = slope
        self.offset = offset

    def mv_to_kg(self, mv_value):
        return((mv_value - self.offset) * (1.0/self.slope))

    def get_bias(self):
        return self.offset

    def set_bias(self, bias):
        self.offset = bias

"""
@title LoadCellAccumulator
@description Handles all load cells and accumulated data from arduino into an 'always most recent' stream

"""
class LoadCellAccumulator:

    """
    @title init NOT DIRECTLY CALLED. NO ARGS. Does standard setup.
    """
    def __init__(self, _numLoadCells = 7):
        print "Initializing from LCA.py"
        self.numLoadCells = _numLoadCells
        self.measuredLoads = []
        self.ser = self.instantiate_arduino_listener()
        #print "SELF.SER", self.ser
        self.startTime = time.time()
        # load cell calibration profile
        self.hasUpdated = False
        self.loadCellDataCollector = self.loadCellThread(
            self.updateLoadsFromSensors)
        self.loadCellDataCollector.start()
        print "measuredLoads Now: ", self.measuredLoads
        self.lcpArray = []

    """
    @title loadCellThread
    @description Just boilerplate to run threads for each of the load cells
    TBH still don't understand why we didn't just make LoadCellAccumulator implement threading
    It would have made perfect sense as one big old thread since all the wrapper is
    doing is creating a smaller internal thread to the larger outer class. ???
    """
    class loadCellThread(threading.Thread):

        def __init__(self, func):
            threading.Thread.__init__(self)
            self.func = func

        def run(self):
            self.func()

    # defined on april 9th to match with arduino's ordering of datapoints.
    # Accepts slighly different lengths and orientations of the incoming data.
    # strict on string characteristics
    def serial_dataline_has_correct_composition(self, dataline):
        #print "Dataline", dataline
        correct_decimal_locations = find(dataline, ",") == [10, 21, 32, 43, 54, 65] ### The indices where commas are suppose to be; To ensure data is received n right format in case some comma gets dropped or length is'nt right ###
        correct_length = len(dataline) in [78]
        if not correct_length or not correct_decimal_locations:
            print('Nonstandard Dataformat received:')
            print("Length observed: %i"%len(dataline))
            print(find(dataline, ","))
        print "correct_decimal_locations and correct_length", correct_decimal_locations, correct_length
        return(correct_decimal_locations and correct_length)

    def decode_and_split_to_list(self, line, numLoadCells):
        loads = [x.strip() for x in bytes.decode(line).split(',')]
        if self.isFloatable(loads) and len(loads) == numLoadCells:
            self.set_hasUpdatedToTrue()
            return(loads)
    # extracts the loads from the sensors via CSV splitting and carriage
    # returns. uses readLIies.

    # if you haven't already toggled it as True, print to console and toggle
    # hasUpdated to True.
    def set_hasUpdatedToTrue(self):
        if self.hasUpdated is False:
            self.hasUpdated = True
            print("LoadCellAccumulator is receiving data")

    def updateLoadsFromSensors(self, numLoadCells=7):
        for line in self.serial_generator(self.ser):
            print "line from serial generator: ",line
            if self.serial_dataline_has_correct_composition(line):
                try:
                    self.measuredLoads = self.decode_and_split_to_list(
                        line, numLoadCells)
                except UnicodeDecodeError:
                    pass

    #@param stringList a list of strings where we expect each element to be cast-able to a float.
    #@return true only if the above is possible
    def isFloatable(self, stringList):
        try:
            [float(x) for x in stringList]
            return True
        except:
            pass
        return False

    def err_if_arduino_not_plugged_in(self, ACMPorts):
        if not len(ACMPorts) >= 1:
            raise Exception('Arduino is not plugged into a USB port.')

    #@return the arduino path to usb. will have ACM in the string name
    def findPortname(self):
        comports = [x[0] for x in list_ports.comports()] ### list_ports.comports() returns all the available serial ports ###
        ACMPorts = [port for port in comports if "ACM" in port]
        self.err_if_arduino_not_plugged_in(ACMPorts)
        print('Arduino Connection: Good')
        return ACMPorts[0]

    def isCollectingData(self):
        awoken = abs(time.time() - self.startTime) > 2.5
        return(self.hasUpdated is True)

    # use python -m serial.tools.list_ports to show the ports that are available for serial communication
    # @param portname string, by default '/dev/ttyACM1'
    # @return an IO: wrapper around a Serial object.
    def instantiate_arduino_listener(self):
        print "Instantiating Arduino"
        portname = self.findPortname()
        ser = serial.Serial(portname, 115200,
                            timeout=None,
                            bytesize=serial.EIGHTBITS,
                            parity=serial.PARITY_NONE,
                            stopbits=serial.STOPBITS_ONE)
        ser.nonblocking()
        return(ser)

    """
    @title getLoadsArray
    @description Called externally to get the most recent loads array.
    @return arrayOfCurrentLoads
    """
    def getLoadsArray(self):
        return np.asarray(self.measuredLoads).astype(np.float)

    """
    @title get_calibratedTensions
    @description gets the list of post-calibrated tensions. IE the usable values
    @return calibratedTensions post-calibration load-cell measurements
    """
    def get_calibratedTensions(self):
        loads = self.getLoadsArray()
        print "Loads", loads
        print "lcpArray", lcpArray
        calibratedTensions = [self.lcpArray[i].mv_to_kg(
            loads[i]) for i in range(len(self.lcpArray))]
        return(calibratedTensions)

    """
    Same as getLoadsArray but doesn't use numpy. ???
    """
    def get_uncalibrated_loads(self):
        loads = self.getLoadsArray()
        return(loads)
    """
    @title serial_generator
    @description simple generator that always just grabs a serial line when one is available.
    """
    def serial_generator(self, serial_object):
        while True:
            yield serial_object.readline()
        serial_object.close()
