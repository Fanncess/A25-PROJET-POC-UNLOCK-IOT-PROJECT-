from pad4pi import rpi_gpio
import time
from CharLCD1602 import CharLCD1602
import RPi.GPIO as GPIO
import time
import subprocess
from gpiozero import MotionSensor

#JOUER L'ENIGME VOCALE
TEXT = "Voici l'énigme ultime pour dévérouiller la porte. " \
"Quelle est la date de création du Cégep Beauce Appalaches?"
PROPOSITION ="A. 1969 OU B. 1972 OU C. 1990."
BONNE_REPONSE = "Bonne réponse. Porte déverrouillée."
MAUVAISE_REPONSE = "Mauvaise réponse. Essayez encore."
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
ANNONCE_BONNE_REPONSE = [
    "espeak",
    "-v", "mb-fr1",
    "-s", "130",
    "-p", "30",
    "-a", "200",
    BONNE_REPONSE
]
ANNONCE_MAUVAISE_REPONSE= [
    "espeak",
    "-v", "mb-fr1",
    "-s", "130",
    "-p", "30",
    "-a", "200",
    MAUVAISE_REPONSE
]

#CONFIGURER LE RELAIS
RELAY_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW)

#CONFIGURER LE CAPTEUR DE MOUVEMENT
SENSOR_PIN = 18
SENSOR = MotionSensor(SENSOR_PIN)
time.sleep(2)  

#INITIALISER LE CODE
lcd1602 = CharLCD1602()
lcd1602.init_lcd(addr=None, bl=1)
lcd1602.clear()

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
            subprocess.run(ANNONCE_BONNE_REPONSE)    
            ouvrir_porte()
        else:
            lcd1602.clear()
            subprocess.run(ANNONCE_MAUVAISE_REPONSE)
    
        time.sleep(2)
        ENTERED_CODE = ""


keypad.registerKeyPressHandler(key_pressed)

def ouvrir_porte():
    GPIO.output(RELAY_PIN, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(RELAY_PIN, GPIO.LOW)   

def lancer_enigme():
    lcd1602.clear() 
    lcd1602.write(0, 0, 'Enigme lance')  
    subprocess.run(COMMANDE_TEXT)   
    subprocess.run(PROPOSITION_REPONSES)    
    lcd1602.write(0,0, "Entrez la reponse:")    

try:
    while True:
        mouvement_detecte = SENSOR.motion_detected
        if mouvement_detecte == True:
            lcd1602.clear()
            lcd1602.write(0, 0, 'Mouvement detecte')
            time.sleep(3)
            mouvement_detecte = SENSOR.motion_detected
            lancer_enigme()     
        else:
            SENSOR.wait_for_motion()       
            lcd1602.clear()
            lcd1602.write(0, 0, 'En attente de mouvement')
        
except KeyboardInterrupt:
    GPIO.cleanup()
    SENSOR.close()