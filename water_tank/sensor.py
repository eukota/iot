'''
Sensor reading class for interacting with the sensor
Inits sensor and allows for reading distance
'''
import RPi.GPIO as GPIO
import time
import logging

SPEED_OF_SOUND_IN_CM_PER_S = 34300.0

class Sensor:
    def __init__(self, pin_trigger, pin_echo, sleep_time=5) -> None:
        GPIO.setmode(GPIO.BOARD)
        self.PIN_TRIGGER = pin_trigger
        self.PIN_ECHO = pin_echo
        GPIO.setup(self.PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(self.PIN_ECHO, GPIO.IN)
        GPIO.output(self.PIN_TRIGGER, GPIO.LOW)
        logging.debug("Waiting for sensor to settle")
        time.sleep(sleep_time)
        logging.debug("Calculating distance")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        GPIO.cleanup()

    def pulse(self, interval = 0.00001) -> None:
        GPIO.output(self.PIN_TRIGGER, GPIO.HIGH)
        time.sleep(interval)
        GPIO.output(self.PIN_TRIGGER, GPIO.LOW)

    def distance_in_inches(self) -> float:
        self.pulse()
        while GPIO.input(self.PIN_ECHO)==0:
                pulse_start_time = time.time()
        while GPIO.input(self.PIN_ECHO)==1:
                pulse_end_time = time.time()
        pulse_duration = pulse_end_time - pulse_start_time
        roundtrip_distance_in_cm = SPEED_OF_SOUND_IN_CM_PER_S * pulse_duration
        self.distance_in_inches = roundtrip_distance_in_cm / 2.0 / 2.54
        return self.distance_in_inches

