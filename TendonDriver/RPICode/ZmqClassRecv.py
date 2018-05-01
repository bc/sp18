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
import random

class ZmqClassRecv:
	
	class ZmqRecvThread(threading.Thread):
		def __init__(self, func):
			threading.Thread.__init__(self)
			self.func = func
		def run(self):
			self.func()

	# extracts the loads from the sensors via CSV splitting and carriage returns. uses readLIies.
	def RecvTargetForces(self):
		context = zmq.Context()
		self.socket = context.socket(zmq.REQ)
		self.socket.connect("tcp://192.168.2.1:5558")
		TIMEOUT = 10000
		self.start_time = time.time()

		while True:
			self.socket.send_string("request")
			poller = zmq.Poller()
			poller.register(self.socket, zmq.POLLIN)
			evt = dict(poller.poll(TIMEOUT))
			if evt:
				if evt.get(self.socket) == zmq.POLLIN:
					rcvTargetForces = self.socket.recv(zmq.NOBLOCK)
					# print('targetForces %s' % str(rcvTargetForces))
					try:
						targetForceList = [forceVal.strip() for forceVal in rcvTargetForces.split(',')]
						prospectiveForceList = np.asarray(targetForceList).astype(np.float)
						if self.forces_are_valid(prospectiveForceList):
							# print(prospectiveForceList)
							self.targetForces = prospectiveForceList
					except UnicodeDecodeError:
						pass
				continue
			time.sleep(0.5)
			self.socket.close()
			self.socket = context.socket(zmq.REQ)
			self.socket.connect("tcp://192.168.2.1:5558")

	def possible_to_absolute_value_all_vals(self, prospectiveForceList):
		try:
			absolute_valued = [np.abs(x) for x in prospectiveForceList]
			return(True)
		except:
			return(False)
	def forces_are_valid(self, prospectiveForceList):
		if len(prospectiveForceList) != 7:
			return(False)
		if not self.possible_to_absolute_value_all_vals(prospectiveForceList):
			return(False)
		return(True)

	def __init__(self):
		self.numLoadCells = 7
		self.measuredLoads = []
		self.updatedLoads = " " 
		self.startTime = time.time()
		self.targetForces = [0.5,0.5,0.5,0.5,0.5,0.5,0.5]
		self.hasUpdated = False
		self.zmqRecv = self.ZmqRecvThread(self.RecvTargetForces)
		self.zmqRecv.start()

	
	def isCollectingData(self):
		return abs(time.time() - self.startTime) > 2.5 and self.hasUpdated is True

	def serial_generator(self, serial_object):
		while True:
			yield serial_object.readline()
		serial_object.close()
		#returns most updated version of target forces 
	def getTargetForces(self):
			return(self.targetForces)

#try:
#    lca = LoadCellAccumulator()
#    Zmq = ZmqClassRecv(lca)
#except KeyboardInterrupt:
#    Zmq.zmqRecv.socket.close()
	

