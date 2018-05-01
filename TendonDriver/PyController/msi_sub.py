#! /usr/local/bin/python3
import sys
import zmq
import time
import random
import pdb

if len(sys.argv) > 1:
    ip_string = sys.argv[1]

if len(sys.argv) > 2:
    port_int = sys.argv[2]

socket_string = "tcp://%s:%s" % (ip_string, str(port_int))

context = zmq.Context()
socket = context.socket(zmq.REQ)
print("connecting to %s" % socket_string)
socket.connect(socket_string)

TIMEOUT = 10000

while True:
    socket.send_string("request")
    pdb.set_trace()
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    evt = dict(poller.poll(TIMEOUT))
    if evt:
        if evt.get(socket) == zmq.POLLIN:
            response = socket.recv(zmq.NOBLOCK)
            print(response)
            continue
    time.sleep(0.5)
    socket.close()
    socket = context.socket(zmq.REQ)
    socket.connect(socket_string)
