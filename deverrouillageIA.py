from picamera2 import Picamera2
import time
import os
import sys
import requests 
from moteur import Moteur
from MQTT.mqtt_publisher import Mqtt_Publisher

# --- Configuration ---


IMAGE_PATH = "./tmp/scan.jpg" 

moteur = Moteur(18)
serrure_control = Mqtt_Publisher()

os.makedirs(os.path.dirname(IMAGE_PATH), exist_ok=True) 


def analyze_image(image_path):
    """
    Sends the image file to the Azure Custom Vision endpoint for prediction.
    Returns "GOOD", "BAD", or "NONE".
    """

    try:
        with open(image_path, "rb") as img:
            print(f"Sending {image_path} to Azure for analysis...")
            response = requests.post(
                AZURE_ENDPOINT,
                headers={
                    "Prediction-Key": AZURE_PREDICTION_KEY,
                    "Content-Type": "application/octet-stream"
                },
                data=img.read()
            )
        response.raise_for_status() 
        
        data = response.json()
        predictions = data.get("predictions", []) 
        
        if not predictions:
            print("Azure response contained no predictions.")
            return "NONE"

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Azure or processing request: {e}")
        return "NONE" 
    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        return "NONE" 
    except Exception as e:
        print(f"Error processing Azure response: {e}")
        return "NONE"

    
    best_tag = None
    best_confidence = 0.0

    print("--- Detailed Detections ---")
    for prediction in predictions: 
        tag = prediction.get("tagName", "N/A")
        confidence = prediction.get("probability", 0.0)
        
        print(f"| Detected: {tag} with {confidence:.2%} confidence")
        
        if confidence > best_confidence:
            best_confidence = confidence
            best_tag = tag

    print("---------------------------")
    print(f"**BEST DETECTION:** {best_tag} with **{best_confidence:.2%}** confidence")
    
    if best_confidence < 0.70:
        print("Validation result: **No bill found** (Best confidence below 70%).")
        return "NONE" 
        
    elif best_tag == "mauvais":
        print("🛑 Validation result: Image is classified as 'mauvais' (bad).")
        return "BAD" 
        
    else:
        if best_tag in ["5", "10", "20", "50", "100"]:
            print(f"Validation result: **Good bill found** ({best_tag}).")
            return "GOOD" 
        else:
            print(f"Validation result: A potentially good/other object was detected ({best_tag}).")
            return "NONE"


picam2 = Picamera2()
picam2.start()
print("Camera started. Press Ctrl+C to stop.")
moteur.close()
moteur.open()
compteur = 1 

while True:
    print("\n--- New Capture Cycle ---")
    print("Say cheese!")
    time.sleep(1)

    
    try:
        picam2.capture_file(IMAGE_PATH) 
        print(f"Picture {compteur} was taken and saved to {IMAGE_PATH}!")
        
        result_type = analyze_image(IMAGE_PATH)
        
        if result_type == "BAD":
            print("🚨 **ACTION REQUIRED:** Bill classified as 'mauvais' (bad). Trigger REJECTION.")
           
        elif result_type == "GOOD":
            print("✅ **ACTION:** Good bill found. Triggering acceptance cycle.")
            moteur.close() 
            moteur.open() 
            serrure_control.send_unlock_signal()
            
        else: 
            print("No bill detected or confidence too low. No motor action taken.")
            
        
    except Exception as e:
        print(f"An error occurred during capture or analysis: {e}")
        
    compteur = compteur + 1
   
    time.sleep(5)