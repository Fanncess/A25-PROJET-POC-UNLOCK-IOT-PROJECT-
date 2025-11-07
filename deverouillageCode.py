from pad4pi import rpi_gpio
import time

CODE_SECRET = "1234"
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
    global ENTERED_CODE
    if key == "*":
        ENTERED_CODE = ""
        print("Code réinitialisé.")
        return
    
    if len(ENTERED_CODE) >= len(CODE_SECRET):
        print("Code trop long, réinitialisez avec '*'.")
        return

    ENTERED_CODE += key
    
    if ENTERED_CODE == CODE_SECRET and len(ENTERED_CODE) == len(CODE_SECRET):
        print("Code correct, déverrouillage...")
    elif ENTERED_CODE != CODE_SECRET and len(ENTERED_CODE) == len(CODE_SECRET):
        print("Code incorrect, essayez encore.")

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
    time.sleep(1)
"""
