
from LoadCellAccumulator import LoadCellAccumulator
import serial
import pdb
import threading
import io
import sys
import time
from serial.tools import list_ports
import numpy as np
import zmq

ip = '192.168.2.10'
port = '5556'

class ZmqClass:

    class ZmqThread(threading.Thread):

        def __init__(self, func, _lca):
            self.lca = _lca
            threading.Thread.__init__(self)
            self.func = func

        def run(self):
            self.func()

    # extracts the loads from the sensors via CSV splitting and carriage
    # returns. uses readLines.
    def SendLoadsFromSensors(self):
        # instantiate the zmq connection to Unity as PUB
        global ip, port
        context = zmq.Context()
        self.socket = context.socket(zmq.PUB)
        # in future write code to find the correct IP address and port
        self.socket.bind("tcp://192.168.2.10:5556") ### "tcp://%s:%s" %(ip, port) ###

        while True:
            if self.lca.isCollectingData():
                loads = self.lca.get_calibratedTensions()
                toSend = "["
                for value in loads:
                    toSend += str(value) + ","
                toSend = toSend[:-1]
                toSend += "]"
                self.socket.send(toSend)
                time.sleep(0.005)

    def __init__(self, _lca):
        self.lca = _lca
        self.numLoadCells = 7
        self.measuredLoads = []
        self.updatedLoads = " "
        self.startTime = time.time()
        self.hasUpdated = False
        self.zmqSender = self.ZmqThread(self.SendLoadsFromSensors, self.lca)
        self.zmqSender.start()
        print("Current libzmq version is %s" % zmq.zmq_version())
        print("Current  pyzmq version is %s" % zmq.__version__)

    def isCollectingData(self):
        elapsed_time = abs(time.time() - self.startTime)
        return elapsed_time > 2.5 and self.hasUpdated is True

    def serial_generator(self, serial_object):
        while True:
            yield serial_object.readline()
        serial_object.close()

# try:
#    lca = LoadCellAccumulator()
#    zmq = ZmqClass(lca)
# except KeyboardInterrupt:
#    zmq.zmqSender.socket.close()
