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

#Botón
BUTTON_PIN = D1

# Cantidad de valores a graficar
maxValues = 100

# Tiempo entre mediciones
sampleTime = 1

# Modos de visualizacion
modes = ["Values", "PlotTemp", "PlotHum"]

####################  Funciones ###################

def readButton ():
    # Lee el User Button de la placa de expansion en D1
    button = Pin (D1, Pin.IN, Pin.PULL_UP)
    return (button.value())
    
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
        
def showTH (temp, hum):
    # Muestra TyH con bitmaps
    tempStr = f"{temp:.1f}"
    humStr  = f"{hum:.0f}"

    #Borra display
    #display.clear()

    #Imprime valores con numeros grandes
    display.draw_text(5, 31, tempStr, perfect, False)
    display.draw_text(85, 31, humStr, perfect, False)
    
    #Mostrar bitmaps
    display.draw_bitmap("images/TempIcon.mono", 25, 0, 32, 32, True)
    display.draw_bitmap("images/HumIcon.mono",  85, 0, 32, 32, True)

    #Actualizar pantalla
    display.present()
    

def plotHum ():
    # Grafica los valores de humedad
    
    maxHum = 100
    
    #display.clear()
    display.draw_rectangle(20, 4, 104, 56, invert=False)
    #Ventana para imprimir 100 x 54
    
    #Escala de valores de humedad
    display.draw_text(0, 0, "100", fixed, False)
    display.draw_text(5, 28, "50", fixed, False)
    display.draw_text(10, 54, "0", fixed, False)
    
    #Titulo
    display.draw_text(5, 15, "H", fixed, False)

    #Plotear los valores almacenados
    x = 22
    for i in listTH:
        h = int (i[1]*56/maxHum)  #Escalar
        display.draw_vline(x, 5, 56-h, invert=True)
        display.draw_vline(x, 60-h, h, invert=False)
        x=x+1
    
    display.present ()

def plotTemp ():
    # Grafica los valores de temperatura
    
    maxTemp = 50
    
    #display.clear()
    display.draw_rectangle(20, 4, 104, 56, invert=False)
    #Ventana para imprimir 100 x 54
    
    #Escala de valores de humedad
    display.draw_text(5, 0, "50", fixed, False)
    display.draw_text(5, 28, "25", fixed, False)
    display.draw_text(10, 54, "0", fixed, False)
    
    #Titulo
    display.draw_text(5, 15, "T", fixed, False)
    
    #Plotear los valores almacenados
    x = 22
    for i in listTH:
        h = int (i[0]*56/maxTemp)  #Escalar
        display.draw_vline(x, 60-h, h, invert=False)
        x=x+1
    
    display.present ()

####################  Código principal  ###################

#Crear objeto I2C
i2c = SoftI2C(freq=400000, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN)) 

#Crear objeto display
display = Display(i2c=i2c, width=128, height=64)

#Crear objeto sensor
sensorTH = DHT11 (Pin(DHT11_PIN))

# Carga fonts
perfect = XglcdFont('fonts/PerfectPixel_23x32.c', 23, 32)
fixed   = XglcdFont('fonts/FixedFont5x8.c',5,8)

# Crear objeto lista para guardar los valores para el gráfico
listTH = deque ([], maxValues)  #No usa maxlen=

# Arranca mostrando valores
modeIndex = 0

# Loop
while (True):
    
    # Medir temperatura y humedad
    sensorTH.measure ()
     
    #beep ()
    
    # Separar valores
    temp = sensorTH.temperature()
    hum  = sensorTH.humidity()
    
    # Guardarlo en la lista (deque)
    listTH.append ((temp,hum))
  
    # Imprimir por consola
    print (temp,"grados")
    print (hum ,"%")
    
    if (readButton()==0):
        beep ()
        modeIndex = (modeIndex + 1) % len (modes)
        display.clear()

    if (modes[modeIndex] == "Values"):
        showTH (temp, hum)
    elif (modes[modeIndex] == "PlotTemp"):
        plotTemp ()
    else:
        plotHum ()
            
   

    #print (button.value())

    # Esperar para la próxima medición
    sleep(sampleTime)
