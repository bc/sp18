import zmq
import pickle
import random
import time
import numpy as np

def instantiate_zmq_publisher(port=12345):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)
    print('Initializing ZMQ pubstream socket')
    return(socket)

def publish_observation(init_socket, messagedata):
    topic = b"map"
    pickled_contents = pickle.dumps(messagedata)
    #print "pickled_contents",pickled_contents, type(pickled_contents)
    try:
        init_socket.send_multipart([topic, pickled_contents])
        time.sleep(0.1)
    except Exception:
        print('Issue in publish_observation')
