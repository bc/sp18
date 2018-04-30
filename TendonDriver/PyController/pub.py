import pdb
import zmq
import sys
import time
import pickle
import numpy as np

port = "5556"
if len(sys.argv) > 1:
    port = sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:%s" % port)


def publish_loop(initialized_socket, sleep_time_seconds):
    while True:
        topic = b"map"
        messagedata = np.random.uniform(0.0, 10.0, 7)
        # print("%d %d" % (topic, messagedata[0]))
        print(messagedata)
        initialized_socket.send_multipart([topic, pickle.dumps(messagedata)])
        time.sleep(sleep_time_seconds)


try:
    publish_loop(socket, 1e-2)
except KeyboardInterrupt:
    socket.unbind()
    socket.close()
finally:
    print("Socket closed?")
    print(str(socket.closed))
