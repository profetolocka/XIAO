# Mide valores de temperatura y humedad usando el módulo Grove DHT11
# Muestra en OLED de base de expansion usando lib ssd1306 oficial

# Pines
D5 = 7

from machine import Pin, SoftI2C
from time import sleep
from dht import DHT11
from ssd1306 import SSD1306_I2C #Libreria oficial


#Crea objeto I2C
i2c = SoftI2C(scl=Pin(7), sda=Pin(6), freq=100000)  #Inicializa i2c

#Crea objeto oled
Display = SSD1306_I2C (128, 64, i2c)


sensorTH = DHT11 (Pin(D5))

while (1):
    sensorTH.measure ()  #Mide
    
    print (sensorTH.temperature(),"grados")
    print (sensorTH.humidity (),"%")
    
    Display.fill (0)

    Display.text ("Temp=",10,10,1)
    Display.text (str(sensorTH.temperature()),50,10,1)
    Display.text ("Hum=",10,20,1)
    Display.text (str(sensorTH.humidity ()),50,20,1)
    Display.show()
    
    sleep (5)



