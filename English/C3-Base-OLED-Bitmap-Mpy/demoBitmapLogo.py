#Bitmap image demo. Displays the Seeed Studio logo

from time import sleep
from machine import Pin, SoftI2C 
from ssd1306 import Display

#Create I2C object
i2c = SoftI2C(freq=400000, scl=Pin(7), sda=Pin(6))  #Pins for the XIAO ESP32-C3

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