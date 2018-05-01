import time
import pdb
import pickle
import sys
import zmq

ip = "169.254.12.240"
port = "5556"


if len(sys.argv) > 1:
    ip = sys.argv[1]

if len(sys.argv) > 2:
    port = sys.argv[2]

def initialize_sub_socket(ip, port, topic_filter=b"map"):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket_string = "%s:%s" % (ip, port)
    print("Connecting to %s" % socket_string)
    #you can run this multiple times to receive from multiple ports
    socket.connect("tcp://" + socket_string)
    socket.setsockopt(zmq.SUBSCRIBE, topic_filter)
    return(socket)

socket = initialize_sub_socket(ip,port)
start = time.time()
count = 0

def receive_and_depickle(socket):
    [topic, msg] = socket.recv_multipart()
    message = pickle.loads(msg, encoding="latin1")
    return(message)

while 1:
    message = receive_and_depickle(socket)
    
    # count += 1
    # if count % 1==0:
    #     elapsed_time = time.time() - start
    #     amortized_rate = count / elapsed_time
    #     print("Msg: %s |Messages per second: %s" % (count,str(amortized_rate)))
    #     #flush the amortized rate buffer every 5 seconds
    #     if elapsed_time > 5:
    #         start = time.time()
    #         count = 0
    #     print(msg2)
