# Sensor de temperatura y humedad con modulo Grove DHT11
# Muestra valores en OLED de placa de expansión
# Usa fonts grandes y bitmaps

from time import sleep
from machine import Pin, SoftI2C 
from ssd1306 import Display

#Crear objeto I2C
i2c = SoftI2C(freq=400000, scl=Pin(7), sda=Pin(6))  #Pines de la XIAO ESP32-C3

#Crear objeto display
display = Display(i2c=i2c, width=128, height=64)

while (True):

    #Mostrar bitmap
    #display.draw_bitmap("images/seeedLogo.mono", 0, 0, 116, 64)
    #display.present()
    #sleep(10)

    #Borrar buffer
    display.clear_buffers()

    #Mostrar bitmap
    display.draw_bitmap("images/seeedLogo.mono", 0, 0, 116, 64, invert=True)
    display.present()
    sleep(10)
