# Author: Ernesto Tolocka (profe Tolocka)
# Date: 15-12-2024
# Description: Temperature and humidity sensor with RP2040 and Grove DHT11 module
# 	Displays values on OLED of expansion board
# 	Uses large fonts and bitmaps
# License: MIT

# Pin name and GPIO mappings
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

# RP2040 I2C pins
PIN_SDA = D4
PIN_SCL = D5

# DHT11 connection pin
PIN_DHT11 = D7

from time import sleep
from machine import Pin, SoftI2C 
from ssd1306 import Display
from xglcd_font import XglcdFont
from dht import DHT11

# Create I2C object
i2c = SoftI2C(freq=400000, scl=Pin(PIN_SCL), sda=Pin(PIN_SDA)) 

# Create display object
display = Display(i2c=i2c, width=128, height=64)

# Create sensor object
sensorTH = DHT11(Pin(PIN_DHT11))

# Load large font
perfect = XglcdFont('fonts/PerfectPixel_23x32.c', 23, 32)

# Loop
while (True):
    
    sensorTH.measure()  # Measure temperature and humidity from the DHT11
    
    temp = sensorTH.temperature()
    hum  = sensorTH.humidity()
    
    print(temp, "degrees")
    print(hum, "%")
    
    tempStr = f"{temp:.1f}"
    humStr  = f"{hum:.0f}"

    # Clear buffer
    display.clear_buffers()
    
    # Display temperature and humidity values on OLED
    display.draw_text(5, 31, tempStr, perfect, False)
    display.draw_text(85, 31, humStr, perfect, False)
    
    # Display bitmaps
    display.draw_bitmap("images/TempIcon.mono", 25, 0, 32, 32, True)
    display.draw_bitmap("images/HumIcon.mono",  85, 0, 32, 32, True)

    # Update screen
    display.present()

    sleep(10)
    