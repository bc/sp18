import pickle 
import sys
import zmq

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)
    
if len(sys.argv) > 2:
    port1 =  sys.argv[2]
    int(port1)

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Collecting updates from weather server...")
socket.connect("tcp://localhost:%s" % port)

if len(sys.argv) > 2:
    socket.connect("tcp://localhost:%s" % port1)

topicfilter = b"map"
socket.setsockopt(zmq.SUBSCRIBE, topicfilter)

# Process 5 updates
while 1:
    [topic,msg] = socket.recv_multipart()
    msg2 = pickle.loads(msg)
    print(topic)
    # print(msg)
    print(msg2)