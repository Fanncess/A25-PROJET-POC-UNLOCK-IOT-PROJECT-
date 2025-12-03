from pirc522 import RFID
import RPi.GPIO as GPIO
import time
import csv
import os
from MQTT.mqtt_publisher import Mqtt_Publisher

serrure_controle = Mqtt_Publisher()

AUTHORIZED_CARDS = [
    "1A5BAFAD43",
]

rdr = RFID()
util = rdr.util()
util.debug = False
LED_GREEN = 13 
LED_RED = 37  

LED_PULSE = 5
LOG_FILE = "access_log.csv"


#GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_GREEN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(LED_RED, GPIO.OUT, initial=GPIO.LOW)


AUTHORIZED_SET = { ''.join(ch for ch in uid if ch.isalnum()).upper() for uid in AUTHORIZED_CARDS }

def uid_to_str(uid):
    """Transforme liste d'entiers UID en chaîne hex sans séparateur (MAJ)"""
    return ''.join(f"{x:02X}" for x in uid)

def log_access(uid_str, result):
    exists = os.path.exists(LOG_FILE)
    with open(LOG_FILE, "a", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if not exists:
            writer.writerow(["timestamp", "uid", "result"])
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), uid_str, result])

def indicate_result(authorized):
    """Allume la LED verte ou rouge pendant LED_PULSE secondes."""
    if authorized:
        GPIO.output(LED_GREEN, GPIO.HIGH)
        serrure_controle.send_unlock_signal()
        time.sleep(3)
        GPIO.output(LED_GREEN, GPIO.LOW)
    else:
        GPIO.output(LED_RED, GPIO.HIGH)
        time.sleep(LED_PULSE)
        GPIO.output(LED_RED, GPIO.LOW)



print("Démarrage du lecteur RFID (pirc522). Approche une carte...")
try:
    while True:
        rdr.wait_for_tag()
        #print("tag detecte")
        (error, tag_type) = rdr.request()
        #print("carte detecte")
        if not error:
            (error, uid) =rdr.anticoll()
            print("aucun collision")

            if not error and uid:
                uid_str = uid_to_str(uid)
                print(f"[INFO] UID détecté: {uid_str}")
                if uid_str in AUTHORIZED_SET:
                    print("[ACCESS] Accès autorisé")
                    log_access(uid_str, "AUTHORIZED")
                    indicate_result(True)
                            
                else:
                    print("[ACCESS] Accès refusé")
                    log_access(uid_str, "DENIED")
                    indicate_result(False)
                
        time.sleep(3)
except KeyboardInterrupt:
    print("\nArrêt demandé")
finally:
    GPIO.output(LED_GREEN, GPIO.LOW)
    GPIO.output(LED_RED, GPIO.LOW)
    GPIO.cleanup()
    try:
        rdr.cleanup()
    except Exception:
        pass
    print("Nettoyage terminé. Au revoir.")





