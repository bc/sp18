import zmq
import time
import random
import pickle

def server_push(port="5558"):
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:%s" % port)
    print("Running server on port: ", port)
    while True:
        message = socket.recv()
        print("Received : %s" % message) #(message).decode("utf-8")
        referenceForces = []
        randomRef = random.uniform(0,1)
        referenceForces.append([randomRef for i in range(7)])
        pickled_contents = pickle.dumps(referenceForces)
        socket.send(pickled_contents)
        time.sleep(10)

server_push()
