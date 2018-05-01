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

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket_string = "%s:%s" % (ip, port)

print("Awaiting data from %s" % socket_string)

#you can run this multiple times to receive from multiple ports
socket.connect("tcp://" + socket_string)

topic_filter = b"map"
socket.setsockopt(zmq.SUBSCRIBE, topic_filter)

# Process 5 updates
start = time.time()
count = 0
while 1:
    [topic, msg] = socket.recv_multipart()
    msg2 = pickle.loads(msg, encoding="latin1")
    count += 1
    if count % 1==0:
        elapsed_time = time.time() - start
        amortized_rate = count / elapsed_time
        print("Msg: %s |Messages per second: %s" % (count,str(amortized_rate)))
        #flush the amortized rate buffer every 5 seconds
        if elapsed_time > 5:
            start = time.time()
            count = 0
        print(msg2)
    # print(topic)
    # print(msg2)
