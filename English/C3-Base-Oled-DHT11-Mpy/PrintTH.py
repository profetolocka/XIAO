# Measures temperature and humidity values using the Grove DHT11 module
# Displays on OLED from expansion board using the official ssd1306 library

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

from machine import Pin, SoftI2C
from time import sleep
from dht import DHT11
from ssd1306 import SSD1306_I2C  # Official library

#Create I2C object
i2c = SoftI2C(scl=Pin(D5), sda=Pin(D4), freq=100000)  #Initialize I2C

#Create OLED object
Display = SSD1306_I2C(128, 64, i2c)

# Create sensor object
sensorTH = DHT11(Pin(D7))

while (1):
    sensorTH.measure()  #Measure
    
    print(sensorTH.temperature(), "degrees")
    print(sensorTH.humidity(), "%")
    
    Display.fill(0)

    Display.text("Temp=", 10, 10, 1)
    Display.text(str(sensorTH.temperature()), 50, 10, 1)
    Display.text("Hum=", 10, 20, 1)
    Display.text(str(sensorTH.humidity()), 50, 20, 1)
    Display.show()
    
    sleep(5)