# Temperature and humidity sensor with Grove DHT11 module
# Displays values on the expansion board OLED
# Uses large fonts and bitmaps

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
from xglcd_font import XglcdFont

from dht import DHT11

#Create I2C object
i2c = SoftI2C(freq=400000, scl=Pin(D5), sda=Pin(D4))  #Pins for the XIAO ESP32-C3

#Create display object
display = Display(i2c=i2c, width=128, height=64)

#Create sensor object
sensorTH = DHT11(Pin(D7))

# Load large font
perfect = XglcdFont('fonts/PerfectPixel_23x32.c', 23, 32)

while (True):
    
    sensorTH.measure()  #Measure temperature and humidity with DHT11
    
    temp = sensorTH.temperature()
    hum  = sensorTH.humidity()
    
    print(temp, "degrees")
    print(hum, "%")
    
    tempStr = f"{temp:.1f}"
    humStr  = f"{hum:.0f}"

    #Clear buffer
    display.clear_buffers()
    
    #Display temperature and humidity values on OLED
    display.draw_text(5, 31, tempStr, perfect, False)
    display.draw_text(85, 31, humStr, perfect, False)
    
    #Display bitmaps
    display.draw_bitmap("images/TempIcon.mono", 25, 0, 32, 32, True)
    display.draw_bitmap("images/HumIcon.mono",  85, 0, 32, 32, True)

    #Update screen
    display.present()

    sleep(10)