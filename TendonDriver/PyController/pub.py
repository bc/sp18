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
    count = 0
    while True:
        topic = b"map"
        messagedata = np.random.uniform(0.0, 10.0, 100)
        # print("%d %d" % (topic, messagedata[0]))
        # print(messagedata)
        pickled_contents = pickle.dumps(messagedata)
        initialized_socket.send_multipart([topic, pickled_contents])
        time.sleep(sleep_time_seconds)
        if count % 1000==0:
            print(count)

try:
    publish_loop(socket, 0.0)
except KeyboardInterrupt:
    socket.unbind()
    socket.close()
finally:
    print("Socket closed?")
    print(str(socket.closed))
