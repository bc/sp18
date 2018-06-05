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
import pickle

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
		global port
		try:
			context = zmq.Context()
			self.socket = context.socket(zmq.REP)
			self.socket.bind("tcp://*:%s" %port) 
			TIMEOUT = 10000
			self.start_time = time.time()

			while True:
				poller = zmq.Poller()
				poller.register(self.socket, zmq.POLLIN)
				evt = dict(poller.poll(TIMEOUT))
				#print "evt", evt
				if evt:
					if evt.get(self.socket) == zmq.POLLIN:
						rcvReferenceForces = self.socket.recv(zmq.NOBLOCK)
						rcvReferenceForces = (pickle.loads(rcvReferenceForces))
						rcvReferenceForces = rcvReferenceForces[0]
						self.socket.send_string("received newRefForce")
						print('newReferenceForces %s' % str(rcvReferenceForces))
						try:
							### convert the received target forces and convert them into a np array of floats
							#referenceForceList = [forceVal.strip() for forceVal in rcvReferenceForces.split(',')]
							prospectiveForceList = np.asarray(rcvReferenceForces).astype(np.float)
							if self.forces_are_valid(prospectiveForceList):
								print(prospectiveForceList)
								self.referenceForces = prospectiveForceList
						except UnicodeDecodeError:
							pass
					continue
				time.sleep(0.5)
		except KeyboardInterrupt:
			self.socket.close()

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
		self.referenceForces = [0.5,0.5,0.5,0.5,0.5,0.5,0.5]
		self.hasUpdated = False
		self.zmqRecv = self.ZmqRecvThread(self.RecvTargetForces)
		self.zmqRecv.start()

	### Removed the serial_generator() and isCollectingData() ####

	#returns most updated version of target forces
	#TODO change targetForces to referenceForces
	def getTargetForces(self):
			return(self.referenceForces)

#try:
#    lca = LoadCellAccumulator()
#    Zmq = ZmqClassRecv(lca)
#except KeyboardInterrupt:
#    Zmq.zmqRecv.socket.close()
