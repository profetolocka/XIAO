# Measures temperature and humidity values using the Grove DHT11 module
# Displays on OLED from expansion board using the official ssd1306 library

# Pins
D5 = 7

from machine import Pin, SoftI2C
from time import sleep
from dht import DHT11
from ssd1306 import SSD1306_I2C  # Official library

#Create I2C object
i2c = SoftI2C(scl=Pin(7), sda=Pin(6), freq=100000)  #Initialize I2C

#Create OLED object
Display = SSD1306_I2C(128, 64, i2c)

# Create sensor object
sensorTH = DHT11(Pin(D5))

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