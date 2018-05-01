import time
import pdb
import pickle
import sys
import zmq

ip = "169.254.12.240"
port = "5556"
if len(sys.argv) > 1:
    port = sys.argv[1]
    int(port)

if len(sys.argv) > 2:
    port1 = sys.argv[2]
    int(port1)

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket_string = "%s:%s" % (ip, port)

print("Awaiting data from %s" % socket_string)
socket.connect("tcp://" + socket_string)

if len(sys.argv) > 2:
    socket.connect("tcp://169.254.12.240:%s" % port1)

topic_filter = b"map"
socket.setsockopt(zmq.SUBSCRIBE, topic_filter)

# Process 5 updates
start = time.time()
count = 0
while 1:
    [topic, msg] = socket.recv_multipart()
    msg2 = pickle.loads(msg, encoding="latin1")
    count += 1
    elapsed_time = time.time() - start
    amortized_rate = count / elapsed_time
    print("Messages per second: %s" % str(amortized_rate))
    # print(topic)
    # print(msg2)
