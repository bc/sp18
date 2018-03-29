import RPi.GPIO as GPIO
from PySerialTest import LoadCellAccumulator
from time import sleep
import pdb
try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print("Error! Must sudo!")
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(True)

# @param stepper_tuple the first value is the step pin, and the second value is the direction pin
# @param initial_frequency set by default to 50Hz. integer value
def set_GPIO_settings(stepper_tuple, initial_frequency=50):
	GPIO.setup(stepper_tuple[0], GPIO.OUT)
	GPIO.setup(stepper_tuple[1], GPIO.OUT)
	PWM_CONTROLLER = GPIO.PWM(stepper_tuple[0], initial_frequency)
	PWM_CONTROLLER.start(50.0)
	return(PWM_CONTROLLER)
def stop_all_motors(pwm_controller_list):
	[x.stop() for x in pwm_controller_list]


stepper_step_dir = [(3,5), (13,15), (11,12), (18,16), (19,21),(23,24),(31,29)]

pwm_controller_list = [set_GPIO_settings(motor) for motor in stepper_step_dir]

minnimum = 200
maxx = 3400
curr = 1700
up = True

lca = LoadCellAccumulator()
try:
	while True:
		if(lca.isCollectingData()):
			vals = lca.getLoads()
			print(vals)
			for i in range(0,7):
				pwm_controller_list[i].ChangeFrequency(float(vals[i])*1000.0 + 50.0)
			sleep(.02)

except KeyboardInterrupt:
	pass
stop_all_motors(pwm_controller_list)
GPIO.cleanup()
