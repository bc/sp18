import zmq
import pickle
import time
import numpy as np
from bokeh.layouts import layout, row, gridplot, column
import bokeh
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import RadioGroup
from bokeh.layouts import widgetbox
from bokeh.plotting import figure
import random
import pdb


source = ColumnDataSource(dict(x=[], muscle_0=[], muscle_1=[], muscle_2=[], muscle_3=[], muscle_4=[],muscle_5=[], muscle_6=[] ))
radio_group = RadioGroup(labels=["50", "100", "200", "500", "1000"], active=0)
rollover_lt = 50

ip = '10.42.0.82'
port = '12345'

def initialize_sub_socket(topic_filter=b"map"):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket_string = "%s:%s" % (ip, port)
    #print("Connecting to %s" % socket_string)
    #you can run this multiple times to receive from multiple ports
    socket.connect("tcp://%s:%s" %(ip, port))
    socket.setsockopt_string(zmq.SUBSCRIBE,'')
    #print('Set ZMQ Subscriber with topic filter')
    return(socket)

def change_lt():
    #print("####################HERE##########################")
    global radio_group,rollover_lt
    vals = [50,100,200,500,1000]
    ind = radio_group.active
    rollover_lt = vals[ind]

radio_group.on_change('active', lambda attr, old, new: change_lt())

ctr = []
def update_data():
    global ctr, socket, source, rollover_lt
    [topic, msg] = socket.recv_multipart()
    message = pickle.loads(msg, encoding="latin1")
    # print("MESSAGE", message)
    print("MESSAGE[0][0]", message[0][0])
    # print("MESSAGE[0][3]", message[0][3], type(message[0][3]))

    ctr = list(range(len(message[0][0])))
    # measuredForces = message[0][0]
    # targetForces = message[0][1]
    # commands = message[0][2]

    #new_data = dict(x=[ctr], muscle_0=[message[0][0]], muscle_1=[message[0][1]], muscle_2 = [message[0][2]])
    new_data = dict(x=[ctr],muscle_0=[message[0][0][0]],muscle_1=[message[0][0][1]],muscle_2=[message[0][0][2]],muscle_3=[message[0][0][3]],muscle_4=[message[0][0][4]],muscle_5=[message[0][0][5]],muscle_6=[message[0][0][6]])
    source.stream(new_data, rollover_lt)
    print("streamed data: ",len(source.data['x']))


def update():
    global main_layout
    for i in range(7):
        main_layout.children[i] = generate_figure()[i]

def generate_figure():
    global source
    update_data()
    colors = ["#762a83","#76EEC6","#53868B","#FF1493","#ADFF2F","#292421","#FFE1FF"]
    figlist = []

    for i in range(7):
        fig = figure(plot_width=250, plot_height=250, title=None)
        muscle = 'muscle_%s' %i
        hist, edges = np.histogram(source.data[muscle])
        fig.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], fill_color=colors[i])
        figlist.append(fig)

    return (figlist)

socket = initialize_sub_socket()

btn_layout = row(radio_group)
main_layout = row(generate_figure())
final_layout = row(main_layout, btn_layout)

curdoc().add_periodic_callback(update, 1000)
curdoc().add_root(final_layout)
