from deverrouillage import Deverrouillage
import time
lockControl = Deverrouillage()
compte = 0

while True:
    time.sleep(1)
    print(compte)
    compte = compte + 1