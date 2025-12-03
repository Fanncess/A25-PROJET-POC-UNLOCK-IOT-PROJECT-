"""
#test listener
from deverrouillage import Deverrouillage
import time
lockControl = Deverrouillage()
compte = 0

while True:
    time.sleep(1)
    print(compte)
    compte = compte + 1

#test publisher
from MQTT.mqtt_publisher import Mqtt_Publisher
import time
publisher = Mqtt_Publisher("localhost", 1883)

while True:
    time.sleep(4)
    publisher.send_lock_signal()
    time.sleep(4)
    publisher.send_unlock_signal()
"""

# Explications:
"""
Il faudra que tous les codes séparer utilise la classe Mqtt_Publisher pour gerer le controle de la serrure
- la classe s'initiallise avec l'adresse IP du broker (à décider mais ça pourra etre le portable d'anne-marie, adresse ip devra etre changé dans le code a chaque cours) et le port 1883
- il y a deux methode importante : send_lock_signal et send_unlock_signal qui remplaceront le GPIO.HIGH et GPIO.LOW du relais

Ensuite! 2 options pour gerer le déverrouillage
Tout se passe dans la classe Deverrouillage et cest elle qui envoie les signals au GPIO
    1_ Meilleure mais plus long: on fait un code qui est roule sur un pi seul qui a la serrure de connecté et tout ce quil fait cest écouter le broket et réagir au besoin
    2_ Moins nice et je suis pas certaine si ça va marcher, mais on initialise la classe dans le code déja connecté a la serrure et ce code devra rouler pour TOUS LES AUTRES CODE
    exemple: le code qui déverrouille avec un code devra rouler en même temps que le code qui déverrouille avec la camera et l'argent
"""