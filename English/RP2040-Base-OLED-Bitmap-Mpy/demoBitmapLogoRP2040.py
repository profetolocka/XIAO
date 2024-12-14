# Bitmap image demo. Displays the Seeed Studio logo
# Uses a XIAO RP2040 board

# GPIO pin names
D0 = 26
D1 = 27
D2 = 28
D3 = 29
D4 = 6
D5 = 7
D6 = 0
D7 = 1
D8 = 2
D9 = 4
D10 = 3

# I2C pins on the RP2040
SDA_PIN = D4
SCL_PIN = D5

from time import sleep
from machine import Pin, SoftI2C 
from ssd1306 import Display

# Create I2C object
i2c = SoftI2C(freq=400000, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN))  

# Create display object
display = Display(i2c=i2c, width=128, height=64)

while (True):

    # Display bitmap
    display.draw_bitmap("images/seeedLogo.mono", 0, 0, 116, 64)
    display.present()
    sleep(10)

    # Clear buffer
    display.clear_buffers()

    # Display bitmap (inverted)
    display.draw_bitmap("images/seeedLogo.mono", 0, 0, 116, 64, invert=True)
    display.present()
    sleep(10)