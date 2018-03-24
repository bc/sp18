import serial
import pdb
import io

import asyncio
import serial_asyncio

# use python -m serial.tools.list_ports to show the ports that are available for serial communication



class Output(asyncio.Protocol):

	def __init__(self):
		self.readings_list = []
		self.errors_list = []
		
	def connection_made(self, transport):
    #	ser_io = io.TextIOWrapper(io.BufferedRWPair(ser,ser,1), newline='\n',line_buffering=True)
		self.transport = transport
		print('port opened', transport)
		transport.serial.rts = False
	def data_received(self, data):
		print('data received', repr(data))
		string_data = bytes.decode(data)
		loads = [x.strip()  for x in string_data.split(',')]
		print(string_data)
		if len(loads) == 7:
			readings_list += [[float(x) for x in loads]]
		else:
			errors_list += [loads]
        #self.transport.close()

	def connection_lost(self, exc):
		print('port closed')
		asyncio.get_event_loop().stop()

loop = asyncio.get_event_loop()
coro = serial_asyncio.create_serial_connection(loop, Output, '/dev/ttyACM1', baudrate=115200,timeout=100,bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()