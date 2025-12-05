import paho.mqtt.client as mqtt

class Mqtt_Publisher:
    def __init__(self, adresse_ip = "10.4.1.199", port= 1883):
        self.adresse_ip = adresse_ip
        self.port = port
        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqttc.on_connect = self.on_connect
        self.mqttc.connect(adresse_ip, port)
        self.mqttc.loop_start()        


    def on_connect(self, client, userdata, flags, reason_code, properties):
        print(f"Connected with result code {reason_code}")

    def send_unlock_signal(self):
        self.mqttc.publish("serrure_controle", 1, qos=1, retain= False) 
    
    def send_lock_signal(self):
        self.mqttc.publish("serrure_controle", 0, qos=1, retain= False) 
