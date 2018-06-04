from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.layouts import gridplot, row, layout, column
import numpy as np
import time
import cProfile
import random
import zmq
import pickle
import pdb
import time

def initialize_sub_socket(ip, port_sub, port_serv, topic_filter=b"map"):
    context = zmq.Context()
    socket_sub = context.socket(zmq.SUB)
    socket_string = "%s:%s" % (ip, port_sub)
    print("Connecting to %s" % socket_string)
    #you can run this multiple times to receive from multiple ports
    socket_sub.connect("tcp://%s:%s" %(ip, port_sub))
    socket_sub.setsockopt(zmq.SUBSCRIBE, topic_filter)
    print('Set ZMQ Subscriber with topic filter')

    socket_pull = context.socket(zmq.REQ)
    socket_pull.connect ("tcp://localhost:%s" % port_serv)
    print("Connected to server with port %s" % port_serv)
    print("Sending dummy request")
    socket_pull.send_string("Hello")
    return(socket_sub, socket_pull)

source = ColumnDataSource(dict(time=[], measured_M0=[],
measured_M1=[],
measured_M2=[],
measured_M3=[],
measured_M4=[],
measured_M5=[],
measured_M6=[],
reference_M0=[],
reference_M1=[],
reference_M2=[],
reference_M3=[],
reference_M4=[],
reference_M5=[],
reference_M6=[]))

i = 0
referenceForces = []
ref_flag = True
def update_data():
    global socket_sub, socket_pull, i, ref_flag, referenceForces
    i = i+1
    #print("IN UPDATE DATA",i+1)
    try:
        #print(socket_sub, socket_pull)
        poller = zmq.Poller()
        poller.register(socket_sub, zmq.POLLIN)
        poller.register(socket_pull, zmq.POLLIN)
        socks = dict(poller.poll())

        if socket_pull in socks and socks[socket_pull] == zmq.POLLIN:
            print("PULLING")
            msg = socket_pull.recv()
            new_referenceForce = (pickle.loads(msg, encoding="latin1"))
            referenceForces = new_referenceForce[0]
            print("## PULL ##",referenceForces)
            ref_flag = False
            print("Recieved control command: %s" % referenceForces)
            socket_pull.send_string(str(time.time()))
            #socket_pull.send("Received reference Force")

        if socket_sub in socks and socks[socket_sub] == zmq.POLLIN:
            print("PUBBING")
            [topic, msg] = socket_sub.recv_multipart()
            #print("VALUES", msg)
            message = (pickle.loads(msg, encoding="latin1"))
            print("values", message)
            measuredForces = message[0][0]
            if ref_flag:
                referenceForces = message[0][1]
            #residualForces = [message[0][0][i]-message[0][1][i] for i in range(7)]
            commands = message[0][2]
            timestamp = message[1]
            print("## PUBB ##",referenceForces)
            new_data = dict(time=[timestamp],measured_M0=[measuredForces[0]],measured_M1=[measuredForces[1]],measured_M2=[measuredForces[2]],measured_M3=[measuredForces[3]],measured_M4=[measuredForces[4]],measured_M5=[measuredForces[0]],measured_M6=[measuredForces[6]],reference_M0=[referenceForces[0]],reference_M1=[referenceForces[1]],reference_M2=[referenceForces[2]],reference_M3=[referenceForces[3]],reference_M4=[referenceForces[4]],reference_M5=[referenceForces[5]],reference_M6=[referenceForces[6]])

            source.stream(new_data, 100)

    except KeyboardInterrupt:
        socket_sub.close()
        socket_pull.close()

def update():
    global main_layout
    for i in range(7):
        main_layout.children[i] = create_figline()[i]

def create_figline():
    global source
    update_data()
    colors = ["#762a83","#76EEC6","#53868B","#FF1493","#ADFF2F","#292421","#EE6A50"]
    figlist = []
    for muscle_index in range(7):
        fig = figure(plot_width=2000, plot_height=180, title=None)
        fig.line(source=source, x='time', y='measured_M%s' %muscle_index, line_width=2, alpha=0.85, color=colors[muscle_index])
        fig.line(source=source, x='time', y='reference_M%s' %muscle_index, line_width=2, alpha=0.85, color='blue')
        figlist.append(fig)
    return figlist

ip = '127.0.0.1'
#ip = '10.42.0.82'
port_sub = '1234'
port_serv = '5556'
socket_sub, socket_pull = initialize_sub_socket(ip, port_sub, port_serv)


curdoc().add_periodic_callback(update, 1)
main_layout = column(create_figline(), sizing_mode='scale_width')
curdoc().add_root(main_layout)
