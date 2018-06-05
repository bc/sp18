import zmq
import time
import random
import pickle

ip = '10.42.0.82'
port = '5558'

def push_randomRefForce():
    global ip, port
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://%s:%s" %(ip, port))
    print("Running client on %s:%s" %(ip, port))
    while True:
        referenceForces = []
        randomRef = random.uniform(0,1)
        referenceForces.append([randomRef for i in range(7)])
        pickled_contents = pickle.dumps(referenceForces)
        socket.send(pickled_contents)
        message = socket.recv()
        print("Received : %s" % message) #(message).decode("utf-8")
        time.sleep(10)

push_randomRefForce()
