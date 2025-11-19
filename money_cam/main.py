from picamera2 import Picamera2
import time


picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (1920,1080)},lores={"size": (640,480)},display="lores")
picam2.configure(camera_config)

picam2.start()
compteur = 1
while True:
    print("Say cheese!")
    time.sleep(1)
    picam2.capture_file("photos/money%u.jpg" % compteur)
    print("Picture%u was taken!" % compteur)
    compteur = compteur + 1
    time.sleep(5)