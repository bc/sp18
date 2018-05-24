import zmq
import pickle
import random
import time
import numpy as np

### Currently just spewing random data but meant to help in Visualising the data sent from Rpi ###
def instantiate_zmq_publisher(port=12345):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)
    print('Initializing ZMQ pubstream socket')
    return(socket)


#sample_data = np.random.uniform(0.0, 10.0, 100)

def publish_observation(init_socket, messagedata):
    topic = b"map"

    # messagedata = (np.vstack([measuredForces, targetForces, commands]), time.time())
    #print messagedata #print messagedata[0][0]
    #print("%d %d" % (topic, messagedata[0]))
    pickled_contents = pickle.dumps(messagedata)
    #print "pickled_contents",pickled_contents, type(pickled_contents)

    try:
        init_socket.send_multipart([topic, pickled_contents])
        #time.sleep(0.1)
    except Exception:
        print('Issue in publish_observation')

#init_socket = instantiate_zmq_publisher()
#publish_observation(init_socket)
