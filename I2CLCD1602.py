#!/usr/bin/env python3
########################################################################
# Filename    : I2CLCD1602.py
# Description : Use the LCD display data
# Author      : freenove
# modification: 2023/05/15
########################################################################

from time import sleep, strftime
from CharLCD1602 import CharLCD1602

lcd1602 = CharLCD1602()    
def get_cpu_temp():     # get CPU temperature from file "/sys/class/thermal/thermal_zone0/temp"
 
    return 'allo'

    
def loop():
    lcd1602.init_lcd() 
    count = 0
    while(True):
        lcd1602.clear()
        lcd1602.write(0, 0, 'TEST : ' + get_cpu_temp() )# display CPU temperature

        sleep(1)
def destroy():
    lcd1602.clear()
if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
    