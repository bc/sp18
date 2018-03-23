import RPi.GPIO as GPIO
from time import sleep
try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print("Error! Must sudo!")
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(True)
def set_GPIO_settings(stepper_tuple, initial_frequency=1275):
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

try:
	while True:
		if up:
			curr += 100
			if curr >= maxx:
				up = False
		else:
			curr -= 100
			if curr <= minnimum:
				up = True
		[x.ChangeFrequency(curr) for x in pwm_controller_list]
		sleep(.2)

except KeyboardInterrupt:
	pass
stop_all_motors(pwm_controller_list)
GPIO.cleanup()
