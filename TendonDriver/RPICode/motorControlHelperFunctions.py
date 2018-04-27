import RPi.GPIO as GPIO
import pdb
import time
import numpy as np

# Initial Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
stepper_step_dir = [(3, 5), (13, 15), (11, 12), (18, 16),
                    (19, 21), (33, 36), (32, 31)]
# @param stepper_tuple the first value is the step pin, and the second value is the direction pin
# @param initial_frequency set by default to 50Hz. integer value


def set_GPIO_settings(stepper_tuple, initial_frequency=50):
    GPIO.setup(stepper_tuple[0], GPIO.OUT)
    GPIO.setup(stepper_tuple[1], GPIO.OUT)

    GPIO.output(stepper_tuple[1], GPIO.HIGH)
    PWM_CONTROLLER = GPIO.PWM(stepper_tuple[0], initial_frequency)
    PWM_CONTROLLER.start(50.0)
    return(PWM_CONTROLLER)


def stop_all_motors(pwm_controller_list):
    [x.stop() for x in pwm_controller_list]


def stop_motor(pwm_controller_list, motor_i):
    pwm_controller_list[motor_i].stop()


def setOffsetsOnceLCAIsReady(lca):
    while True:
        if lca.isCollectingData() == True:
            setOffsets(lca)
            break


def loadcellReadToUnits(readVal, unit):
    value = readVal - offsetVals[unit]
    return value / scaleVals[unit]


def loadcellArrayToUnitArray(loads, offset_vector, scale_vector):
    return(scale_vector * loads + offset_vector)

startTime = time.time()
def applyCommandsToMotorDrivers(pwm_controller_list, commandTensions):
    cellIterator = range(len(commandTensions))
    # print(commandTensions)
    global startTime
    if time.time() - startTime > 10:
        pass
        # pdb.set_trace()
    for i in cellIterator:
        changeFrequencyAndDirection(pwm_controller_list[i], commandTensions[i], i)


def changeFrequencyAndDirection(pwm_controller, commandTension, motorNum, minMotorFrequencyAmplitude = 10):
    if commandTension < minMotorFrequencyAmplitude and commandTension > -minMotorFrequencyAmplitude:
        pwm_controller.ChangeDutyCycle(0)
        return
    else:
        pwm_controller.ChangeDutyCycle(50)
    pwm_controller.ChangeFrequency(np.abs(commandTension))
    if commandTension < 0:
        GPIO.output(stepper_step_dir[motorNum][1], GPIO.LOW)
    else:
        GPIO.output(stepper_step_dir[motorNum][1], GPIO.HIGH)


def gen_pwm_controller_list(list_of_step_dir_tuples):
    pwm_controller_list = [set_GPIO_settings(
        motor) for motor in list_of_step_dir_tuples]
    return(pwm_controller_list)
