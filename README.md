# 🔐 UNLOCK – IoT Project

## 📘 Description du projet

UNLOCK est un projet IoT ayant pour objectif de concevoir un **système de déverrouillage intelligent** à l’aide d’un **Raspberry Pi**.  
Le système permet d’ouvrir une porte selon **différentes méthodes de déverrouillage**, toutes reliées en utilisant un **broker MQTT** servant de point central de communication.

Ce projet a été réalisé à des fins **pédagogiques** dans le cadre du cours *Programmation d’objets connectés*.

---

## 🎯 Objectif du projet

Le projet vise à démontrer :
- l’intégration du **matériel et du logiciel** en IoT,
- la communication entre modules via protocole **MQTT**,
- la mise en place de **plusieurs méthodes de déverrouillage** autour d’un même système.

---

## 🧠 Fonctionnement général du système

Le système est composé de plusieurs modules indépendants reliés par un **broker MQTT**.

1. Un module valide un accès (code, énigme, RFID ou détection d’objet).
2. Le module publie un message au broker MQTT dans un sujet "serrure_controle".
3. Le module central est abonné au sujet "serrure_controle" sur le broker.
4. Le module central fait la gestion de la serrure. Il la déverrouille lorsque le sujet auquel il est abonné reçoit le message correspondant.
5. La serrure est déverrouillée pendant un temps défini.
6. La porte se reverrouille automatiquement.

---

## 🧰 Matériel requis

Pour reproduire ce projet, le matériel suivant est nécessaire :

### Matériel principal
- Raspberry Pi  
- Carte micro-SD avec Raspberry Pi OS  
- Alimentation 5V pour Raspberry Pi  

### Déverrouillage par code et énigme
- Clavier matriciel 4 × 4  
- Écran LCD  
- Serrure motorisée (solénoïde)  
- Capteur de mouvement (PIR)  
- Speaker Bluetooth   

### Détection d’objet (IA)
- Caméra Raspberry Pi v2  
- Servo moteur SG90  

### Déverrouillage par RFID
- Lecteur RFID RC522 (SPI)  
- Carte RFID  
- LEDs (rouge et verte)  

### Autres
- Breadboard  
- Fils Dupont  
- Résistances  
- Alimentation 12V (si nécessaire pour la serrure)

---

## 💻 Logiciels requis

- Raspberry Pi OS  
- Python 3  
- Git  
- Broker MQTT (Mosquitto)  

---

## 📦 Librairies et outils utilisés

- `RPi.GPIO` / `lgpio`  
  Gestion des broches GPIO du Raspberry Pi.  
  Utilisé pour lire les boutons, contrôler la serrure motorisée, le servo moteur, les LEDs et le capteur de mouvement.

- `pad4pi`  
  Librairie dédiée à la gestion du **clavier matriciel 4 x 4**.  
  Permet de détecter les touches pressées sans avoir à gérer manuellement les lignes et colonnes du clavier.

- `pi-rc522`  
  Librairie utilisée pour le **lecteur RFID RC522**.  
  Permet de lire l’UID des cartes RFID et de le comparer à une liste de cartes autorisées.

- `spidev`  
  Librairie utilisée pour la **communication SPI**.  
  Nécessaire au fonctionnement du lecteur RFID RC522.

- `picamera2`  
  Librairie permettant de contrôler la **caméra Raspberry Pi v2**.  
  Utilisée pour capturer des images envoyées au service Azure Computer Vision lors de la détection d’objet (billets canadiens).

- `requests`  
  Librairie HTTP utilisée pour communiquer avec des **services externes**, notamment l’API **Azure Computer Vision**.  
  Elle permet d’envoyer les images capturées et de recevoir les résultats d’analyse.

- `CharLCD1602`  
  Librairie utilisée pour le **pilotage de l’écran LCD**.  
  Sert à afficher les messages à l’utilisateur (erreur, succès, instructions, état de la porte).

- `MotionSensor`  
  Module utilisé pour gérer le **capteur de mouvement (PIR)**.  
  Permet de détecter une présence et de déclencher la séquence d’énigme.

- `subprocess`  
  Librairie Python standard utilisée pour exécuter des **commandes système**.  
  Elle est utilisée pour lancer la synthèse vocale via eSpeak.

- `espeak`  
  Outil de **synthèse vocale** utilisé dans le module d’énigme.  
  Il permet de :
  - lire l’énigme à voix haute,
  - annoncer les différents choix de réponses,
  - indiquer verbalement si la réponse est correcte ou non.  
  En cas de bonne réponse, eSpeak annonce **« déverrouillé »** avant l’ouverture de la porte.

- `paho-mqtt`  
  Librairie utilisée pour la **communication MQTT**.  
  Chaque module publie un message au broker MQTT lorsqu’un déverrouillage est validé.
  
- **Azure Computer Vision** : détection d’objet (billets canadiens)  
- **Mosquitto MQTT** : communication entre les modules  

Toutes les dépendances sont listées dans le fichier `requirements.txt`.

---

## 🔍 Détails des méthodes de déverrouillage

### ✅ Déverrouillage par code
- L’utilisateur entre un code à 4 chiffres sur le clavier.
- Le code est validé par le système.
- Un message est affiché sur l’écran LCD.
- Si le code est correct, un message est envoyé dans le sujet "serrure_controle" du broker MQTT.

---

### ✅ Déverrouillage par énigme
- Le capteur de mouvement détecte une présence.
- Une énigme est proposée à l’utilisateur.
- L’utilisateur sélectionne une réponse à l’aide des boutons.
- En cas de bonne réponse un message est envoyé dans le sujet "serrure_controle" du broker MQTT.

---

### ✅ Détection d’objet (IA)
- La caméra Raspberry Pi capture une image.
- L’image est envoyée au service **Azure Computer Vision**.
- Le service analyse l’image afin d’identifier un **billet canadien**.
- Si un billet est reconnu:
  - le servo moteur est activé pour "prendre" l'argent. 
  - Un message est envoyé dans le sujet "serrure_controle" du broker MQTT
- Sinon, l’accès est refusé.

---

### ✅ Déverrouillage par carte RFID
- Le lecteur RC522 lit l’UID de la carte RFID.
- L’UID est comparé à une liste de cartes autorisées.
- Si l’accès est autorisé:
  - Une LED verte s’allume 
  - Un message est envoyé dans le sujet "serrure_controle" du broker MQTT
- Sinon une LED rouge s’allume.
- Les accès sont enregistrés dans un fichier CSV.

---

## 📡 Communication MQTT

Le broker MQTT sert de **point central** du système.
- Chaque module publie un message lorsqu’un accès est validé.
- Le module principal est abonné aux messages.
- Lorsqu’un message est reçu dans le sujet du broker, la porte est déverrouillée puis reverrouillée.

---

## 📁 Organisation du projet

Le dépôt GitHub contient :
- les scripts Python pour chaque méthode de déverrouillage,
- différentes classe:
  - Moteur, gère le controle du servo moteur avec le module d'IA
  - Deverrouillage, incluant la classe Mqtt_Subscriber, gère le controle de la serrure
  - Mqtt_Publisher, importée dans chaque script de déverrouillage, gère l'envoie des messages dans le sujet sur le broker
  - Mqtt_Subscriber, importée dans le script controllant la serrure, gère l'abonnement au sujet sur le broker
- un fichier `requirements.txt`,
- ce fichier README,
- des fichiers utilitaires (affichage LCD, journalisation).

---

## ▶️ Reproduire le projet

Pour reproduire le projet :
1. Préparer le Raspberry Pi avec Raspberry Pi OS.
2. Installer Python et Git.
3. Installer Mosquitto (broker MQTT).
4. Cloner le dépôt GitHub.
5. Installer les librairies à l’aide du fichier `requirements.txt`.
6. Brancher les composantes matérielles.
7. Lancer le broker MQTT.
8. Exécuter les modules souhaités.

---

## ⚠️ Limites du projet

- Sécurité RFID basée uniquement sur l’UID.
- La détection d’objet dépend de la qualité de la caméra et de l’IA.
- Projet conçu à des fins pédagogiques uniquement.

---

## ✅ Conclusion

Ce projet démontre comment un **Raspberry Pi**, des capteurs, des actionneurs et des services cloud peuvent être combinés afin de créer un **système de déverrouillage intelligent IoT**.  
Grâce à ce dépôt GitHub et à cette documentation, le projet peut être compris, reproduit et adapté.

---

## 👥 Équipe

Projet réalisé par :
- Anne-Marie Robert  
- Jessie Velleux  
- Gaelle Miora Ranaivo  
- Fannceska Jeudy  
- Étchri Semane-Dogbé
