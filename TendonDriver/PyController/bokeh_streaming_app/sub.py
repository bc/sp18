import time
import pdb
import pickle
import sys
import zmq

def initialize_sub_socket(ip, port, topic_filter=b"map"):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket_string = "%s:%s" % (ip, port)
    print("Connecting to %s" % socket_string)
    #you can run this multiple times to receive from multiple ports
    socket.connect("tcp://" + socket_string)
    socket.setsockopt(zmq.SUBSCRIBE, topic_filter)
    print('Set ZMQ Subscriber with topic filter')
    return(socket)


def receive_and_depickle(socket):
    [topic, msg] = socket.recv_multipart()
    message = pickle.loads(msg, encoding="latin1")
    return(message)

# socket = initialize_sub_socket(ip,port)
# while 1:
#     message = receive_and_depickle(socket)