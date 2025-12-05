import RPi.GPIO as GPIO
import time

class Moteur():
    def __init__(self, pin):
        self.SERVO_PIN = pin  
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SERVO_PIN, GPIO.OUT)

        self.pwm = GPIO.PWM(self.SERVO_PIN, 50)
        self.pwm.start(0)

    def set_angle(self, angle):
        duty_cycle = (angle / 18) + 2.5 
        GPIO.output(self.SERVO_PIN, True)
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.5) 
        GPIO.output(self.SERVO_PIN, False)
        self.pwm.ChangeDutyCycle(0)


    def close(self):
        self.set_angle(0)


    def open(self):
        self.set_angle(65)
