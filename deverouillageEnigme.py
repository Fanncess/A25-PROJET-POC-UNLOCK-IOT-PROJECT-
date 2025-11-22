from pad4pi import rpi_gpio
import time
from CharLCD1602 import CharLCD1602
import RPi.GPIO as GPIO
import time
import subprocess

#JOUER L'ENIGME VOCALE
TEXT = "Voici l'énigme ultime pour dévérouiller la porte. " \
"Quelle est la date de création du Cégep Beauce Appalaches?"
PROPOSITION ="A. 1969 OU B. 1972 OU C. 1990."
COMMANDE_TEXT = [
    "espeak",
    "-v", "mb-fr1",
    "-s", "130",
    "-p", "30",
    "-a", "200",
    TEXT
]
PROPOSITION_REPONSES = [
    "espeak",
    "-v", "mb-fr1",
    "-s", "130",
    "-p", "30",
    "-a", "200",
    PROPOSITION
]

#CONFIGURER LE RELAIS
RELAY_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW)

#INITIALISER LE CODE
lcd1602 = CharLCD1602()
lcd1602.init_lcd(addr=None, bl=1)
lcd1602.clear()
subprocess.run(COMMANDE_TEXT)
subprocess.run(PROPOSITION_REPONSES)
lcd1602.write(0, 0, 'Entrer la reponse:')

#CONFIGURER LE CODE SECRET
REPONSE = "C" 
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
        lcd1602.write(0,1,"Entrez la réponse")
        return

    ENTERED_CODE += str(key)
    lcd1602.write(0, 0, 'Code: ' + ENTERED_CODE)
    
    if len(ENTERED_CODE) == len(REPONSE):
        if ENTERED_CODE == REPONSE :
            lcd1602.clear()
            lcd1602.write(0, 0, 'Bonne reponse!')
            lcd1602.write(0, 1, 'Deverouille...')
            GPIO.output(RELAY_PIN, GPIO.HIGH)
            time.sleep(5)
            GPIO.output(RELAY_PIN, GPIO.LOW)

             
        else:
            lcd1602.clear()
            lcd1602.write(0, 0, 'Mauvaise reponse!')
            lcd1602.write(0, 1, 'Reessayez...')
    
        time.sleep(2)
        ENTERED_CODE = ""
        lcd1602.clear()
        subprocess.run(COMMANDE_TEXT)
        subprocess.run(PROPOSITION_REPONSES)
        lcd1602.write(0,0, "Entrez la reponse:")

keypad.registerKeyPressHandler(key_pressed)

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()