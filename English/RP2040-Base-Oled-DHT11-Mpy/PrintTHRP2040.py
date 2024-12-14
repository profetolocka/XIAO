# Author: Ernesto Tolocka (profe Tolocka)
# Date: 14-12-2024
# Description: Measures temperature and humidity values using the Grove DHT11 module
# 	Displays on OLED from expansion base using the official ssd1306 library
# 	Uses the XIAO RP2040 board
# License: MIT

# Pins
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

# I2C
SDA_PIN = D4
SCL_PIN = D5

# Buzzer
BUZZER_PIN = D3

from machine import Pin, SoftI2C, PWM
from time import sleep
from dht import DHT11
from ssd1306 import SSD1306_I2C  # Official library

# Create I2C object
i2c = SoftI2C(scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=100000)  # Initialize i2c

# Create OLED object
Display = SSD1306_I2C(128, 64, i2c)

# The Grove DHT11 module is connected to D7
sensorTH = DHT11(Pin(D7))

# Makes a beep using the passive buzzer on the expansion board
def beep():
    # Makes a beep on the passive buzzer
    buzzer = PWM(Pin(BUZZER_PIN))
    buzzer.freq(1000)
    buzzer.duty_u16(32768)  # 50% Duty Cycle

    sleep(0.1)
    buzzer.deinit()  # Releases resources

# Loop

while True:
    sensorTH.measure()  # Measure
    
    print(sensorTH.temperature(), "degrees")
    print(sensorTH.humidity(), "%")
    
    Display.fill(0)

    Display.text("Temp=", 10, 10, 1)
    Display.text(str(sensorTH.temperature()), 50, 10, 1)
    Display.text("Hum=", 10, 20, 1)
    Display.text(str(sensorTH.humidity()), 50, 20, 1)
    Display.show()
    
    beep()
    
    sleep(5)