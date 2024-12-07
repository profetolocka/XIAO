#Demo de imagen bitmap. Muestra el logo de Seeed Studio
#Usa una placa XIAO RP2040

#Pines
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

from time import sleep
from machine import Pin, SoftI2C 
from ssd1306 import Display

#Crear objeto I2C
i2c = SoftI2C(freq=400000, scl=Pin(D5), sda=Pin(D4))  #Pines de la XIAO RP2040

#Crear objeto display
display = Display(i2c=i2c, width=128, height=64)

while (True):

    #Mostrar bitmap
    display.draw_bitmap("images/seeedLogo.mono", 0, 0, 116, 64)
    display.present()
    sleep(10)

    #Borrar buffer
    display.clear_buffers()

    #Mostrar bitmap
    display.draw_bitmap("images/seeedLogo.mono", 0, 0, 116, 64, invert=True)
    display.present()
    sleep(10)
