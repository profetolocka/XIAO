#Bitmap image demo. Displays the Seeed Studio logo

#Pin name and GPIO equivalences
D0 = 2
D1 = 3
D2 = 4
D3 = 5
D4 = 6
D5 = 7
D6 = 21
D7 = 20
D8 = 8
D9 = 9
D10 = 10

from time import sleep
from machine import Pin, SoftI2C 
from ssd1306 import Display

#Create I2C object
i2c = SoftI2C(freq=400000, scl=Pin(D5), sda=Pin(D4))  #Pins for the XIAO ESP32-C3

#Create display object
display = Display(i2c=i2c, width=128, height=64)

while (True):

    #Display bitmap
    display.draw_bitmap("images/seeedLogo.mono", 0, 0, 116, 64)
    display.present()
    sleep(10)

    #Clear buffer
    display.clear_buffers()

    #Display bitmap
    display.draw_bitmap("images/seeedLogo.mono", 0, 0, 116, 64, invert=True)
    display.present()
    sleep(10)