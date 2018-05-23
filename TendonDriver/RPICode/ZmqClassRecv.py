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


ip = '192.168.2.1'
port = '5558'

class ZmqClassRecv:

	class ZmqRecvThread(threading.Thread):
		def __init__(self, func):
			threading.Thread.__init__(self)
			self.func = func
		def run(self):
			self.func()

	# extracts the loads from the sensors via CSV splitting and carriage returns. uses readLIies.
	def RecvTargetForces(self):
		#print "RecvTargetForces"
		global ip, port
		context = zmq.Context() ### Contexts help manage created sockets & the number of threads ZeroMQ uses behind the scenes. Create one when initializing a process and destroy when process terminates0. Can be shared between threads, in fact, are the only ZeroMQ objects that can safely do this ###
		self.socket = context.socket(zmq.REQ)
		self.socket.connect("tcp://%s:%s" %(ip, port)) ### "tcp://%s:%s" %(ip, port) ### "tcp://192.168.2.1:5558"
		TIMEOUT = 10000
		self.start_time = time.time()

		while True:
			self.socket.send_string("request")
			poller = zmq.Poller()
			poller.register(self.socket, zmq.POLLIN)
			evt = dict(poller.poll(TIMEOUT))
			#print "evt", evt
			if evt:
				if evt.get(self.socket) == zmq.POLLIN:
					rcvTargetForces = self.socket.recv(zmq.NOBLOCK)
					print('targetForces %s' % str(rcvTargetForces))
					try:
						### convert the received target forces and convert them into a np array of floats
						targetForceList = [forceVal.strip() for forceVal in rcvTargetForces.split(',')]
						prospectiveForceList = np.asarray(targetForceList).astype(np.float)
						if self.forces_are_valid(prospectiveForceList):
							print(prospectiveForceList)
							self.targetForces = prospectiveForceList
					except UnicodeDecodeError:
						pass
				continue
			time.sleep(0.5)
			### commenting reconnecting socket within while
			self.socket.close()
			self.socket = context.socket(zmq.REQ)
			self.socket.connect("tcp://192.168.2.1:5558")

	def possible_to_absolute_value_all_vals(self, prospectiveForceList):
		try:
			absolute_valued = [np.abs(x) for x in prospectiveForceList] ### uses np.abs() to check if received force is a valid no. ###
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
		print "Initializing ZmqClassRecv"
		self.numLoadCells = 7
		self.measuredLoads = []
		self.updatedLoads = " "
		self.startTime = time.time()
		self.targetForces = [0.5,0.5,0.5,0.5,0.5,0.5,0.5]
		self.hasUpdated = False
		self.zmqRecv = self.ZmqRecvThread(self.RecvTargetForces)
		self.zmqRecv.start()

	### Removed the serial_generator() and isCollectingData() ####

	#returns most updated version of target forces
	def getTargetForces(self):
			return(self.targetForces)

#try:
#    lca = LoadCellAccumulator()
#    Zmq = ZmqClassRecv(lca)
#except KeyboardInterrupt:
#    Zmq.zmqRecv.socket.close()
