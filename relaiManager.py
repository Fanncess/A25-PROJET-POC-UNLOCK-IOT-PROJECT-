import time
import RPi.GPIO as GPIO

class RelayManager:
    def __init__(self, pin=17):
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)   

    def unlock(self, duration=3):
        GPIO.output(self.pin, GPIO.HIGH) 
        time.sleep(duration)
        GPIO.output(self.pin, GPIO.LOW)

    def cleanup(self):
        GPIO.cleanup()