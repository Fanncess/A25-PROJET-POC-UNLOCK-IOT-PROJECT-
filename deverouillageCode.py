from pad4pi import rpi_gpio
import time
from CharLCD1602 import CharLCD1602
import RPi.GPIO as GPIO
import time
from MQTT.mqtt_publisher import Mqtt_Publisher
from keypadFactory import create_keypad

#CONFIGURER LE RELAIS
RELAY_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW)

#INITIALISER LE CODE
lcd1602 = CharLCD1602()
lcd1602.init_lcd(addr=None, bl=1)
lcd1602.clear()
lcd1602.write(0, 0, 'SYSTEME PRET')
lcd1602.write(0, 1, 'Entrer le code :')
serrure_controle = Mqtt_Publisher()

#CONFIGURER LE CODE SECRET
CODE_SECRET = "1234" 
ENTERED_CODE = ""

#DEFINITION DE LA FONCTION A APPELER A CHAQUE TOUCHE
def key_pressed(key):
    global ENTERED_CODE
    lcd1602.clear()

    if key == "*":
        ENTERED_CODE = ""
        lcd1602.write(0,0,"Code reset")
        lcd1602.write(0,1,"Entrez le code")
        return

    ENTERED_CODE += str(key)
    lcd1602.write(0, 0, 'Code: ' + ENTERED_CODE)
    
    if len(ENTERED_CODE) == len(CODE_SECRET):
        if ENTERED_CODE == CODE_SECRET :
            lcd1602.clear()
            lcd1602.write(0, 0, 'Code correct!')
            lcd1602.write(0, 1, 'Deverouille...')
            #GPIO.output(RELAY_PIN, GPIO.HIGH)
            serrure_controle.send_unlock_signal()
            time.sleep(3)
            #GPIO.output(RELAY_PIN, GPIO.LOW)

             
        else:
            lcd1602.clear()
            lcd1602.write(0, 0, 'Code incorrect!')
            lcd1602.write(0, 1, 'Reessayez...')
    
        time.sleep(2)
        ENTERED_CODE = ""
        lcd1602.clear()
        lcd1602.write(0,0, "Entrez le code:")

keypad = create_keypad(key_pressed)

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()