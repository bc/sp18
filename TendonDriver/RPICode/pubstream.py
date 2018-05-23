import zmq
import cPickle
import numpy as np

### Currently just spewing random data but meant to help in Visualising the data sent from Rpi ###
def instantiate_zmq_publisher(port=12345):
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:%s" % port)
    print('Initializing ZMQ pubstream socket')
    return(socket)


sample_data = np.random.uniform(0.0, 10.0, 100)

def publish_observation(initialized_socket, messagedata=sample_data):
    topic = b"map"
    # print("%d %d" % (topic, messagedata[0]))
    # print(messagedata)
    pickled_contents = cPickle.dumps(messagedata)
    try:
        initialized_socket.send_multipart([topic, pickled_contents])
    except Exception:
        print('Issue in publish_observation')
