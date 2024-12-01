# Sensor de temperatura y humedad con modulo Grove DHT11
# Muestra valores en OLED de placa de expansión
# Usa fonts grandes y bitmaps

#Equivalencias entre nombres de pines y GPIOs
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

#Crear objeto I2C
i2c = SoftI2C(freq=400000, scl=Pin(7), sda=Pin(6))  #Pines de la XIAO ESP32-C3

#Crear objeto display
display = Display(i2c=i2c, width=128, height=64)

#Crear objeto sensor
sensorTH = DHT11 (Pin(D5))

# Carga font
perfect = XglcdFont('fonts/PerfectPixel_23x32.c', 23, 32)


while (True):
    
    sensorTH.measure ()  #Mide Temperatura y humedad del DHT11
    
    temp = sensorTH.temperature()
    hum  = sensorTH.humidity()
    
    print (temp,"grados")
    print (hum ,"%")
    
    tempStr = f"{temp:.1f}"
    humStr  = f"{hum:.0f}"

    #Borrar buffer
    display.clear_buffers()
    
    display.draw_text(5, 31, tempStr, perfect, False)
    display.draw_text(85, 31, humStr, perfect, False)
    
    #Mostrar bitmaps
    
    display.draw_bitmap("images/TempIcon.mono", 25, 0, 32, 32, True)
    
    display.present()


    #Mostrar bitmap
    #display.draw_bitmap("images/seeedLogo.mono", 0, 0, 116, 64)
    #display.present()
    #sleep(10)

 

    #Mostrar bitmap
    #display.draw_bitmap("images/seeedLogo.mono", 0, 0, 116, 64, invert=True)
    #display.present()
    sleep(10)
