import time
from lcdManager import LCDManager
import RPi.GPIO as GPIO
import time
from MQTT.mqtt_publisher import Mqtt_Publisher
from keypadFactory import create_keypad
from relaiManager import RelayManager

#CONFIGURER LE RELAIS
relay = RelayManager(pin=17)

#INITIALISER LE CODE
lcd1602 = LCDManager()
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
            relay.unlock()   
            serrure_controle.send_unlock_signal()
            time.sleep(3)

             
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