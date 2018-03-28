import serial
import pdb
import threading
import io
import sys
import time
from serial.tools import list_ports

class LoadCellAccumulator:
	
	class loadCellThread(threading.Thread):
		def __init__(self, func):
			threading.Thread.__init__(self)
			self.func = func
		def run(self):
			self.func()

	# extracts the loads from the sensors via CSV splitting and carriage returns. uses readLIies.
	def updateLoadsFromSensors(self):
		countedLines = 0

		for line in self.serial_generator(self.ser):
			if countedLines > self.skipLines:
				try:
					loads = [x.strip() for x in bytes.decode(line).split(',')]
					if(self.isFloatable(loads)):
						if self.is_valid_observation(loads, 7):
							self.measuredLoads = loads
							self.hasUpdated = True
				except UnicodeDecodeError:
					pass
			else:
				countedLines += 1

	#@param stringList a list of strings where we expect each element to be cast-able to a float.
	#@return true only if the above is possible
	def isFloatable(self, stringList):
		try:
			[float(x) for x in stringList]
			return True
		except:
			pass
		return False

	def __init__(self):
		self.numLoadCells = 7
		self.measuredLoads = []
		self.skipLines = 20
		self.ser = self.instantiate_arduino_listener()
		self.startTime = time.time()
		self.hasUpdated = False
		self.loadCellDataCollector = self.loadCellThread(self.updateLoadsFromSensors)
		self.loadCellDataCollector.start()

	#@return the arduino path to usb. will have ACM in the string name
	def findPortname(self):
		comports = [x[0] for x in list_ports.comports()]
		ACMPorts = [port for port in comports if "ACM" in port]
		if len(ACMPorts) >= 1:
			return ACMPorts[0]
		else:
			print("Raised exception")
			raise Exception('Arduino is not plugged into a USB port.')
	
	def isCollectingData(self):
		return abs(time.time() - self.startTime) > 2.5 and self.hasUpdated is True

	# use python -m serial.tools.list_ports to show the ports that are available for serial communication
	##@param portname string, by default '/dev/ttyACM1'
	##@return an IO: wrapper around a Serial object.
	def instantiate_arduino_listener(self):
		portname = self.findPortname()
		ser = serial.Serial(portname, 115200, timeout=None, bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
		ser.nonblocking()	
		return(ser)

	def getLoads(self):
		return self.measuredLoads
	
	def serial_generator(self, serial_object):
		while True:
			yield serial_object.readline()

		serial_object.close()

	def is_valid_observation(self, load_list, num_loadcells):
		if len(load_list) == num_loadcells:
			return(True)
		else:
			return(False)
