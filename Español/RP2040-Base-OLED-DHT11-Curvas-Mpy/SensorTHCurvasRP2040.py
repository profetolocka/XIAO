# Sensor de temperatura y humedad con RP2040 y modulo Grove DHT11
# Muestra valores en OLED de placa de expansión
# Usa fonts grandes y bitmaps
# Muestra curvas de valores de temperatura y humedad

from time import sleep
from machine import Pin, SoftI2C, PWM
from ssd1306 import Display
from xglcd_font import XglcdFont

from collections import deque  #doble-ended queue

from dht import DHT11

################  Constantes ####################

#Equivalencias entre nombres de pines y GPIOs
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

# Pines de I2C de la RP2040
SDA_PIN = D4
SCL_PIN = D5

# Pin de conexion del DHT11
DHT11_PIN = D7

#Buzzer
BUZZER_PIN = D3

# Cantidad de valores a graficar
maxValues = 10

# Tiempo entre mediciones
sampleTime = 10

####################  Funciones ###################

def beep():
    # Hace un beep en el buzzer pasivo
    buzzer = PWM(Pin(BUZZER_PIN))
    buzzer.freq(1000)
    buzzer.duty_u16(32768)  # 50% Duty Cycle

    sleep(0.1)
    buzzer.deinit()

def showList ():
    # Muestra la deque
    for i in listTH:
        print (i)
        
def plotTemp ():
    # Grafica los valores de temperatura
    display.clear()
    display.draw_rectangle(9, 4, 110, 56, invert=False)
    display.present ()

def plotHum ():
    # Grafica los valores de humedad
    pass

####################  Código principal  ###################

#Crear objeto I2C
i2c = SoftI2C(freq=400000, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN)) 

#Crear objeto display
display = Display(i2c=i2c, width=128, height=64)

#Crear objeto sensor
sensorTH = DHT11 (Pin(DHT11_PIN))

# Carga font grande
perfect = XglcdFont('fonts/PerfectPixel_23x32.c', 23, 32)

# Crear objeto lista para guardar los valores para el gráfico
listTH = deque ([], maxValues)  #No usa maxlen=


# Loop
while (True):
    
    # Medir temperatura y humedad
    sensorTH.measure ()
     
    beep ()
    
    # Separar valores
    temp = sensorTH.temperature()
    hum  = sensorTH.humidity()
    
    # Guardarlo en la lista (deque)
    listTH.append ((temp,hum))
    
    # Muestra los valores almacenados
    showList () 
  
# Imprimir por consola
    print (temp,"grados")
    print (hum ,"%")
    
    tempStr = f"{temp:.1f}"
    humStr  = f"{hum:.0f}"

    #Borrar buffer
    display.clear_buffers()
    
    plotTemp ()
    
    #Mostrar valores de temperatura y humedad en OLED
    #display.draw_text(5, 31, tempStr, perfect, False)
    #display.draw_text(85, 31, humStr, perfect, False)
    
    #Mostrar bitmaps
    #display.draw_bitmap("images/TempIcon.mono", 25, 0, 32, 32, True)
    #display.draw_bitmap("images/HumIcon.mono",  85, 0, 32, 32, True)

    #Actualizar pantalla
    display.present()

    # Esperar para la próxima medición
    sleep(sampleTime)
