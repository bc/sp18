import RPi.GPIO as GPIO
from LoadCellAccumulator import LoadCellAccumulator
from time import sleep
import pdb
import sys

try:
	import RPi.GPIO as GPIO
except RuntimeError:
	print("Error! Must sudo!")


#Initial Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(True)
stepper_step_dir = [(3,5), (13,15), (11,12), (18,16), (19,21),(33,36),(32,31)]

#Calibration info
scaleVals = [34.7, 108.0, 43.0, 18.8, 50.0, 10.0, 12.6]
offsetVals = [0,0,0,0,0,0,0]

firstRun = True


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


def loadcellReadToUnits(readVal, unit):
	value = readVal - offsetVals[unit]
	return value / scaleVals[unit]

def setOffsets(loadCells):
	for i in range(0,7):
		reads = []
		for j in range(0,10):
			reads.append(float(loadCells.getLoads()[i]))
			sleep(.015)
		offsetVals[i] = float(sum(reads))/float(len(reads))

pwm_controller_list = [set_GPIO_settings(motor) for motor in stepper_step_dir]

minnimum = 200
maxx = 3400
curr = 1700
up = True

lca = LoadCellAccumulator()
try:
	while True:
		if(lca.isCollectingData()):
			if(firstRun):
				setOffsets(lca)
				firstRun = False
			vals = lca.getLoads()
			debugOut = []
			for i in range(0,7):
				freq = float(loadcellReadToUnits(float(vals[i]), int(i)))
				debugOut.append(freq)
				if freq != 0:		
					if freq < 0:
						GPIO.output(stepper_step_dir[i][1], GPIO.LOW)
						freq *= -1
					else:
						GPIO.output(stepper_step_dir[i][1], GPIO.HIGH)
			
					pwm_controller_list[i].ChangeFrequency(freq)
			sleep(.0125)
			print(debugOut)

except KeyboardInterrupt:
	pass
stop_all_motors(pwm_controller_list)
GPIO.cleanup()
