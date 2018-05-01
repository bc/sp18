import time
import pdb
from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Range1d
from bokeh.plotting import Figure
import numpy as np
import sys
from sub import initialize_sub_socket, receive_and_depickle


def create_figline(muscle_index):
  global fig, source
  colors = ["#762a83",
            "#af8dc3",
            "#e7d4e8",
            "#000000",
            "#d9f0d3",
            "#7fbf7b",
            "#1b7837"]
  fig.line(source=source, x='timestamp', y='measured_M%s' %
           muscle_index, line_width=2, alpha=0.85,
           color=colors[muscle_index])


ip = "169.254.12.240"
port = "12345"

if len(sys.argv) > 1:
  ip = sys.argv[1]

if len(sys.argv) > 2:
  port = sys.argv[2]

source = ColumnDataSource(dict(timestamp=[],
                               measured_M0=[],
                               measured_M1=[],
                               measured_M2=[],
                               measured_M3=[],
                               measured_M4=[],
                               measured_M5=[],
                               measured_M6=[]))


fig = Figure(plot_width=1800, plot_height=1000)
[create_figline(i) for i in range(7)]

fig.y_range = Range1d(-0.5, 3.5)
ct = 0
sine_sum = 0


def forces_to_tuple_entries(forces):
  return([("measured_M%s" % str(i), [forces[i]]) for i in range(len(forces))])


start = time.time()


def sine_updater():
  global ct, sine_sum, socket, start
  # pdb.set_trace()
  # forces,targetforces,commands
  [values, timestamp] = receive_and_depickle(socket)
  [forces, targetforces, commands] = values
  force_dictionary = dict([("timestamp", [timestamp])] +
                          forces_to_tuple_entries(forces))
  # print(message)
  ct += 1
  new_data = force_dictionary
  # pdb.set_trace()
  source.stream(new_data, 400)
  if ct % 100 == 0:
    elapsed_time = time.time() - start
    amortized_rate = ct / elapsed_time
    print("Msg: %s |Messages per second: %s" % (ct, str(amortized_rate)))
    # flush the amortized rate buffer every 5 seconds
    if elapsed_time > 5:
      start = time.time()
      ct = 0


socket = initialize_sub_socket(ip, port)

curdoc().add_root(fig)
curdoc().add_periodic_callback(sine_updater, 0.1)
