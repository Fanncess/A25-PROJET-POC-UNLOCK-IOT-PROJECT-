from pad4pi import rpi_gpio
import time
from CharLCD1602 import CharLCD1602

#INITIALISER LE CODE
lcd1602 = CharLCD1602()
lcd1602.init_lcd(addr=None, bl=1)
lcd1602.clear()
lcd1602.write(0, 0, 'SYSTEME PRET')
lcd1602.write(0, 1, 'ENtrer le code :')

#CONFIGURER LE CODE SECRET
CODE_SECRET = "1234" 
ENTERED_CODE = ""

#CONFIGURER LE CLAVIER
KEYPAD = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]
ROW_PINS = [5, 6, 13, 19]
COL_PINS = [12, 16, 20, 21]
ENTERED_CODE = ""

factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)

#DEFINITION DE LA FONCTION A APPELER A CHAQUE TOUCHE
def key_pressed(key):
    global ENTERED_CODE
    lcd1602.clear()

    if key == "*":
        ENTERED_CODE = ""
        lcd1602.write(0,0,"Code reset")
        lcd1602.write(0,1,"Entrez le code")
        return
    
    if len(ENTERED_CODE) >= len(CODE_SECRET):
        lcd1602.write(0,0,"Code trop long")
        lcd1602.write(0,1,"Reset:*")
        return

    ENTERED_CODE += str(key)
    lcd1602.write(0, 0, 'Code: ' + ENTERED_CODE)
    
    if len(ENTERED_CODE) == len(CODE_SECRET):
        if ENTERED_CODE == CODE_SECRET :
            lcd1602.clear()
            lcd1602.write(0, 0, 'Code correct!')
            lcd1602.write(0, 1, 'Deverouille...')
        else:
            lcd1602.clear()
            lcd1602.write(0, 0, 'Code incorrect!')
            lcd1602.write(0, 1, 'Reessayez...')
    
    time.sleep(2)
    ENTERED_CODE = ""
    lcd1602.clear()
    lcd1602.write(0,0, "Entrez code:")

keypad.registerKeyPressHandler(key_pressed)

print ("Système de déverrouillage par code activé. Saisir '*' pour réinitialiser le code.")
while True :
    time.sleep(0.1) 


"""
import RPi.GPIO as GPIO
import time

RELAY_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

while True :
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    time.sleep(1)
    GPIO.output(RELAY_PIN, GPIO.LOW)
    time.sleep(1)1
"""