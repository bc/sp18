# Reference: https://www.rototron.info/raspberry-pi-stepper-motor-tutorial/


from time import sleep
import pigpio

STEP_0 = 2
DIR_0 = 3

STEP_1 = 14
DIR_1 = 15

STEP_2 = 17
DIR_2 = 18



pi = pigpio.pi()

#Unit 0 setup
pi.set_mode(DIR_0,pigpio.OUTPUT)
pi.set_mode(STEP_0,pigpio.OUTPUT)
pi.write(DIR_0, 1)
pi.set_PWM_dutycycle(STEP_0, 128)
pi.set_PWM_frequency(STEP_0, 8000)

#Unit 1 setup
pi.set_mode(DIR_1,pigpio.OUTPUT)
pi.set_mode(STEP_1,pigpio.OUTPUT)
pi.write(DIR_1, 1)
pi.set_PWM_dutycycle(STEP_1, 128)
pi.set_PWM_frequency(STEP_1, 8000)

#Unit 2 setup
pi.set_mode(DIR_2, pigpio.OUTPUT)
pi.set_mode(STEP_2, pigpio.OUTPUT)
pi.write(DIR_2, 1)
pi.set_PWM_dutycycle(STEP_2, 128)
pi.set_PWM_frequency(STEP_2, 8000)

try:
	while True:
		pi.write(DIR_0,1)
		sleep(2)
		pi.write(DIR_0,0)
		sleep(2)

except KeyboardInterrupt:
	print("\nCtrl-C'd")
finally:
	pi.set_PWM_dutycycle(STEP_0,0)
	pi.set_PWM_dutycycle(STEP_1,0)
	pi.set_PWM_dutycycle(STEP_2,0)
	pi.stop
