import RPi.GPIO as GPIO
import time

class Moteur():
    def __init__(self, pin):
        # Set up the GPIO pin for PWM
        self.SERVO_PIN = pin  # Use GPIO18 (Pin 12)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SERVO_PIN, GPIO.OUT)

        # Start PWM with 50Hz frequency
        self.pwm = GPIO.PWM(self.SERVO_PIN, 50)
        self.pwm.start(0)

    def set_angle(self, angle):
        duty_cycle = (angle / 18) + 2.5  # Convert angle to duty cycle
        GPIO.output(self.SERVO_PIN, True)
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.5)  # Wait for servo to move
        GPIO.output(self.SERVO_PIN, False)
        self.pwm.ChangeDutyCycle(0)


    def close(self):
        self.set_angle(0)


    def open(self):
        self.set_angle(65)
