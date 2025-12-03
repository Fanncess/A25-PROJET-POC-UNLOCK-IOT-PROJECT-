from pad4pi import rpi_gpio
import time
from CharLCD1602 import CharLCD1602
import RPi.GPIO as GPIO
import time
import subprocess
from gpiozero import MotionSensor
from MQTT.mqtt_publisher import Mqtt_Publisher


#JOUER L'ENIGME VOCALE
TEXT = "Voici l'énigme ultime pour dévérouiller la porte. " \
"Quelle est la date de création du Cégep Beauce Appalaches?"
PROPOSITION ="A. 1969 OU B. 1972 OU C. 1990."
BONNE_REPONSE = "Bonne réponse. Porte déverrouillée."
MAUVAISE_REPONSE = "Mauvaise réponse. Essayez encore."

VOICE = ["espeak","-v", "mb-fr1","-s", "130","-p", "30","-a", "200"]

COMMANDE_TEXT = VOICE + [TEXT]
PROPOSITION_REPONSES = VOICE + [PROPOSITION]
ANNONCE_BONNE_REPONSE = VOICE + [BONNE_REPONSE]
ANNONCE_MAUVAISE_REPONSE= VOICE + [MAUVAISE_REPONSE]

#CONFIGURER LE RELAIS
RELAY_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)
GPIO.output(RELAY_PIN, GPIO.LOW)

#CONFIGURER LE CAPTEUR DE MOUVEMENT
SENSOR_PIN = 18
SENSOR = MotionSensor(SENSOR_PIN)
SENSOR.wait_for_no_motion()
time.sleep(2)  

#INITIALISER LE CODE
lcd1602 = CharLCD1602()
lcd1602.init_lcd(addr=None, bl=1)
lcd1602.clear()
serrure_controle = Mqtt_Publisher()


#CONFIGURER LE CODE SECRET
REPONSE = "C" 
ENTERED_CODE = ""
ENIGME_ACTIVE = False
EN_ATTENTE = False

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

def key_pressed(key):
    """Gère l'entrée du clavier."""
    global ENTERED_CODE, ENIGME_ACTIVE, EN_ATTENTE

    if not ENIGME_ACTIVE or not EN_ATTENTE:
        lcd1602.write(0, 1, "Attendez svp")
        return

    if key == "*":
        ENTERED_CODE = ""
        lcd1602.write(0,0,"Code reinitialise")
        lcd1602.write(0,1,"Entrez la reponse:")
        return

    if key in ['A', 'B', 'C', 'D']:
        ENTERED_CODE = key
        lcd1602.write(0, 0, f'Reponse: {ENTERED_CODE}')
        lcd1602.write(0, 1, 'Verification...')
        
        if ENTERED_CODE == REPONSE :
            lcd1602.clear()
            lcd1602.write(0, 0, "SUCCES!")
            subprocess.run(ANNONCE_BONNE_REPONSE)    
            ouvrir_porte()
        else:
            lcd1602.clear()
            lcd1602.write(0, 0, "ECHEC.")
            subprocess.run(ANNONCE_MAUVAISE_REPONSE)
    
        time.sleep(3)

        reset_system()
        
    else:
        lcd1602.write(0, 0, "Touche invalide")
        lcd1602.write(0, 1, "Utilisez A, B, C, D")
        time.sleep(1)
        lcd1602.write(0, 0, f'Reponse: {ENTERED_CODE}')
        lcd1602.write(0, 1, "Entrez la reponse:")

keypad.registerKeyPressHandler(key_pressed)

def ouvrir_porte():
    #GPIO.output(RELAY_PIN, GPIO.HIGH)
    serrure_controle.send_unlock_signal()
    lcd1602.write(0, 1, "Porte ouverte (5s)")
    time.sleep(3)
    #GPIO.output(RELAY_PIN, GPIO.LOW)  
    lcd1602.write(0, 1, "Porte verrouillee")

def lancer_enigme():
    global ENIGME_ACTIVE, EN_ATTENTE

    ENIGME_ACTIVE = True
    EN_ATTENTE = False 

    lcd1602.clear() 
    lcd1602.write(0, 0, 'ENIGME LANCEE')  

    subprocess.run(COMMANDE_TEXT)   
    subprocess.run(PROPOSITION_REPONSES)    

    EN_ATTENTE = True

    lcd1602.clear()
    lcd1602.write(0, 0, "Entrez la reponse:") 
    lcd1602.write(0, 1, " (A, B, C, ou D)")

def reset_system():
    global ENIGME_ACTIVE, EN_ATTENTE, ENTERED_CODE
    ENIGME_ACTIVE = False
    EN_ATTENTE = False
    ENTERED_CODE = ""
    lcd1602.clear()
    lcd1602.write(0, 0, 'En attente de mouvement')

try:
    lcd1602.write(0, 0, 'Systeme pret')
    lcd1602.write(0, 1, 'Attente mouvement...')
    
    while True:
        if SENSOR.motion_detected and not ENIGME_ACTIVE:
            lancer_enigme()
            time.sleep(1) 
        
        time.sleep(0.1) 
        
except KeyboardInterrupt:
    GPIO.cleanup() 
    SENSOR.close()