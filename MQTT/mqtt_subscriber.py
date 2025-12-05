import paho.mqtt.client as mqtt

class Mqtt_Subscriber:
    def __init__(self, adresse_ip="10.4.1.199", port= 1883, handler = None):
        self.adresse_ip = adresse_ip
        self.port = port
        self.handler = handler

        self.mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.mqttc.on_connect = self.on_connect
        self.mqttc.on_message = self.on_message
        self.mqttc.connect(self.adresse_ip, self.port, 60)
        self.mqttc.loop_start()

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(self, client, userdata, flags, reason_code, properties):
        print(f"Connected with result code {reason_code}")
        client.subscribe("serrure_controle")

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        if self.handler is not None:
            self.handler.reception_mqtt(msg.payload.decode())



