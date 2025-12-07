import RPi.GPIO as GPIO
import time
from MQTT.mqtt_subscriber import Mqtt_Subscriber

class Deverrouillage:
    def __init__(self):
        self.mqtt = Mqtt_Subscriber("10.4.1.199",1883, handler=self)
        #CONFIGURER LE RELAIS
        self.RELAY_PIN = 17
        self.UNLOCK_TIME = 3
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.RELAY_PIN, GPIO.OUT)
        self.verrouiller()

    def reception_mqtt(self, message):
        if message == "1":
            self.deverrouiller()
        elif message == "0":
            self.verrouiller()


    def verrouiller(self):    
        GPIO.output(self.RELAY_PIN, GPIO.LOW)
        print("LOCK")

    def deverrouiller(self):    
        GPIO.output(self.RELAY_PIN, GPIO.HIGH)
        print("UNLOCK for %u seconds" %self.UNLOCK_TIME)
        time.sleep(self.UNLOCK_TIME)
        self.verrouiller()

