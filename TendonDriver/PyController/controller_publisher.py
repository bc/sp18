import zmq
import sys
import time
import numpy as np

port = "5556"
if len(sys.argv) > 1:
    port = sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)

while True:
    uar_7d = np.random.uniform(0.0, 10.0, 7)
    socket.send(uar_7d)
    print('published:' + np.array_str(uar_7d))
    time.sleep(1)
