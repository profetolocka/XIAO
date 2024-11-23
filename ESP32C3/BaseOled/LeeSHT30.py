from sht30 import SHT30
from machine import Pin,I2C
from ssd1306 import SSD1306_I2C

sensor = SHT30()

i2cDisp = I2C(scl=Pin(7), sda=Pin(6), freq=100000)  #Inicializa i2c
display = SSD1306_I2C (128, 64, i2cDisp)

display.fill (0)
display.text ("Hola",10,10,1)
display.text ("Mundo",10,20,1)
display.show()

try:
    t, h = sensor.measure()
except SHT30Error as ex:
    print('Error:', ex)