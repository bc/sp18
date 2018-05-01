import LoadCellAccumulator
from ZmqClass import ZmqClass
from ZmqClassRecv import ZmqClassRecv
import pdb
import numpy as np
import time
from genericHelperFunctions import *
from motorControlHelperFunctions import *
from calibrateLoadCells import collectDataAtZeroLoad
from logCSV import *
from pubstream import instantiate_zmq_publisher, publish_observation

# If, god forbid, there's some weird GPIO import error which, apparently
# happens??
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error! Must sudo!")
pwm_controller_list = gen_pwm_controller_list(
    [(3, 5), (13, 15), (11, 12), (18, 16), (19, 21), (33, 36), (32, 31)])

# Zmq is some zmq_generator that has input values coming in on a readline
# like basis


def compose_trigger_command(measuredForce, targetForce, threshold, fixed_speed):
    if np.abs(measuredForce - targetForce) < threshold:
        # print('inthreshold')
        return(0)
    if measuredForce > targetForce:
        return(-fixed_speed)
    else:
        return(fixed_speed)


def compose_P_command(measuredForce, targetForce, threshold, p):
    if np.abs(measuredForce - targetForce) < threshold:
        # print('inthreshold')
        return(0)
    residual = targetForce - measuredForce
    return(p * residual)


from datetime import datetime

# The meaty body loop. This function is CURRENTLY the main control loop
# for the project
"""
@title threshold_loop
@description primary threshold control loop that maintains tensions based on composed commands
@param lca Initialized loadCellAccumulator (See LoadCellAccumulator.py)
@param zmq a generator that supplies values for the threshold loop
@param sleep_time the amount of time to sleep between threshold cycles
@param threshold the actual threshold -- if the value is within threshold of the target, it goes to 0
@param speed overal speed
"""
import cProfile
import re



def threshold_loop(lca, zmq, pubstream_socket, sleep_time, threshold, speed):
    np.set_printoptions(precision=3, suppress=True)
    global pwm_controller_list
    startingTime = datetime.now()
    logFile = initialize_loadcell_log()
    counter = 0
    for targetForces in zmq:
        # targetForces = np.array([1.0]*7)
        measuredForces = lca.get_calibratedTensions()
        commands = [compose_P_command(measuredForces[i], targetForces[
                                      i], threshold, speed) for i in range(7)]
        applyCommandsToMotorDrivers(pwm_controller_list, commands)
        deltaTime = datetime.now() - startingTime
        startingTime = datetime.now()
        loads_to_logCSVline(logFile, measuredForces, targetForces, commands, )
        observation = (np.vstack([measuredForces, targetForces, commands]), time.time())
        tic = datetime.now()
        publish_observation(pubstream_socket, observation)
        toc = datetime.now()
        tic2 = datetime.now()
        if counter % 1000 == 0:
            print(observation)
            print("deltaTime: " + str(deltaTime))
            print("tictoc: " + str(toc-tic))
            print("tictoc2: " + str(tic2-toc))
            print("-------------------")
            counter = 0  # reset
        counter += 1
        time.sleep(sleep_time)

# produce array of values called val


def zmq_generator(zmq_recv):
    while True:
        reference_forces = zmq_recv.getTargetForces()
        yield reference_forces


# Actual script.
try:
    print('LoadCellAccumulator: Initialized')
    lca = LoadCellAccumulator.LoadCellAccumulator()

    time.sleep(1)
    zmq_recv = ZmqClassRecv()
    print('Socket for receiving forces: Acquired')
    zmq_send = ZmqClass(lca)
    pubstream_socket = instantiate_zmq_publisher(12345)
    print('Socket for sending load cell values: Acquired')
    print('Initializing threshold loop')
    while not lca.isCollectingData():
        print('Awaiting stream of data from LoadCellAccumulator')
        time.sleep(0.75)

    multList = [588132.7869,
                205157.3770,
                126567.2131,
                136078.6885,
                160329.5082,
                376400.0000,
                219232.7869]
    offsets = collectDataAtZeroLoad(lca)
    print("Offsets: " + str(offsets))
    lcpArray = [LoadCellAccumulator.LoadCellCalibrationProfile(
        multList[i], offsets[i]) for i in range(len(offsets))]
    lca.lcpArray = lcpArray
    cProfile.run('threshold_loop(lca, zmq_generator(zmq_recv), pubstream_socket, sleep_time=0.01, threshold=0.001, speed=5000)')
    # threshold_loop(lca, zmq_generator(zmq_recv), pubstream_socket,
                   # sleep_time=0.01, threshold=0.001, speed=5000)
except KeyboardInterrupt:
    print("except KeyboardInterrupt")
    stop_all_motors(pwm_controller_list)
    zmq_send.socket.close()
    zmq_recv.socket.close()
    zmq_send.zmq_ctx_destroy()
    zmq_recv.zmq_ctx_destroy()
    GPIO.cleanup()
finally:
    print('finally')
    pass
