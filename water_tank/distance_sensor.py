'''
Distance sensor wrapper for interacting with the ultrasonic sensor.
'''
import RPi.GPIO as GPIO
import time
import logging

SPEED_OF_SOUND_IN_CM_PER_S = 34300.0


class DistanceSensor:
    def __init__(self, pin_trigger, pin_echo, sleep_time=5):
        GPIO.setmode(GPIO.BOARD)
        self.pin_trigger = pin_trigger
        self.pin_echo = pin_echo
        GPIO.setup(self.pin_trigger, GPIO.OUT)
        GPIO.setup(self.pin_echo, GPIO.IN)
        GPIO.output(self.pin_trigger, GPIO.LOW)
        logging.debug("Waiting for sensor to settle")
        time.sleep(sleep_time)
        logging.debug("Calculating distance")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        GPIO.cleanup()

    def pulse(self, interval=0.00001):
        GPIO.output(self.pin_trigger, GPIO.HIGH)
        time.sleep(interval)
        GPIO.output(self.pin_trigger, GPIO.LOW)

    def distance_in_inches(self):
        self.pulse()
        while GPIO.input(self.pin_echo) == 0:
            pulse_start_time = time.time()
        while GPIO.input(self.pin_echo) == 1:
            pulse_end_time = time.time()
        pulse_duration = pulse_end_time - pulse_start_time
        roundtrip_distance_in_cm = SPEED_OF_SOUND_IN_CM_PER_S * pulse_duration
        distance_in_inches = roundtrip_distance_in_cm / 2.0 / 2.54
        return distance_in_inches
