from CharLCD1602 import CharLCD1602

class LCDManager:
    def __init__(self):
        self.lcd = CharLCD1602()
        self.lcd.init_lcd(addr=None, bl=1)
        self.lcd.clear()

    def write(self, line, col, text):
        self.lcd.write(line, col, text)

    def clear(self):
        self.lcd.clear()