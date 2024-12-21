# Author: Ernesto Tolocka (profe Tolocka)
# Creation Date: 15-12-2024
# Description: Program to measure temperature and humidity with the XIAO RP2040 board and the Grove DHT11 module.
#   Displays values on the OLED of the expansion board
#   Uses large fonts and bitmaps
#   Shows current TH, max, min, average, and value graphs
# License: MIT

from time import sleep
from machine import Pin, SoftI2C, PWM
from ssd1306 import Display
from xglcd_font import XglcdFont

from collections import deque  # double-ended queue

from dht import DHT11

################  Constants ####################

# Pin name and GPIO mappings
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

# RP2040 I2C pins
SDA_PIN = D4
SCL_PIN = D5

# DHT11 connection pin
DHT11_PIN = D7

# Buzzer
BUZZER_PIN = D3

# Button
BUTTON_PIN = D1

# Number of values to plot
maxValues = 100

# Time between measurements (sec)
sampleTime = 1

# Display modes
modes = ["Values", "Min", "Max", "Avg", "PlotTemp", "PlotHum"]

####################  Functions ###################

def printBig(temp, hum):
    # Prints two values with a large font
    
    tempStr = f"{temp:.1f}"
    humStr  = f"{hum:.0f}"
    
    # Prints values with large numbers
    # Clears before because the "1" doesn't cover completely
    display.draw_text(5, 31, "     ", perfect, False)
    display.draw_text(5, 31, tempStr, perfect, False)
    display.draw_text(85, 31, "   ", perfect, False)  
    display.draw_text(85, 31, humStr, perfect, False)

def showBitmaps():
    # Displays bitmaps
    display.draw_bitmap("images/TempIcon.mono", 25, 0, 32, 32, True)
    display.draw_bitmap("images/HumIcon.mono",  85, 0, 32, 32, True)

def readButton():
    # Reads the User Button on the expansion board at D1
    # Returns the read value
    return (button.value())
    
def beep():
    # Makes a beep on the passive buzzer
    buzzer = PWM(Pin(BUZZER_PIN))
    buzzer.freq(1000)
    buzzer.duty_u16(32768)  # 50% Duty Cycle

    sleep(0.1)
    buzzer.deinit()  # Releases resources

        
def showTH(temp, hum):
    # Displays current temperature and humidity with bitmaps
    
    # Prints values with a large font
    printBig(temp, hum)
    
    # Displays temp and hum bitmaps
    showBitmaps()

    # Update screen
    display.present()
    

def plotHum(values):
    # Plots humidity values
    
    maxHum = 100
    
    display.draw_rectangle(20, 4, 104, 56, invert=False)
    
    # Humidity scale values
    display.draw_text(0, 0, "100", fixed, False)
    display.draw_text(5, 28, "50", fixed, False)
    display.draw_text(10, 54, "0", fixed, False)
    
    # Title
    display.draw_text(5, 15, "H", fixed, False)

    # Plot the stored values
    x = 22
    for i in values:
        h = int(i[1] * 56 / maxHum)  # Scale
        display.draw_vline(x, 5, 56 - h, invert=True)
        display.draw_vline(x, 60 - h, h, invert=False)
        x = x + 1
    
    display.present()

def plotTemp(values):
    # Plots temperature values
    
    maxTemp = 50
    
    display.draw_rectangle(20, 4, 104, 56, invert=False)
    
    # Temperature scale values
    display.draw_text(5, 0, "50", fixed, False)
    display.draw_text(5, 28, "25", fixed, False)
    display.draw_text(10, 54, "0", fixed, False)
    
    # Title
    display.draw_text(5, 15, "T", fixed, False)
    
    # Plot the stored values
    x = 22
    for i in values:
        h = int(i[0] * 56 / maxTemp)  # Scale
        display.draw_vline(x, 60 - h, h, invert=False)
        x = x + 1
    
    display.present()

def showMin(values):
    # Displays minimum values from the last 100 measurements
    
    # Find the minimums
    tempMin = 50
    humMin = 100
    
    for value in values:
        if (value[0] < tempMin):  # Temperature
            tempMin = value[0]
        if (value[1] < humMin):   # Humidity
            humMin = value[1]
    
    # Prints values with a large font
    printBig(tempMin, humMin)
    
    # Displays bitmaps
    showBitmaps()

    display.draw_text(0, 0, "MIN", fixed, False)

    # Update screen
    display.present()

def showMax(values):
    # Displays maximum values from the last 100 measurements
    tempMax = 0
    humMax = 0
    
    for value in values:
        if (value[0] > tempMax):  # Temperature
            tempMax = value[0]
        if (value[1] > humMax):   # Humidity
            humMax = value[1]
    
    # Prints values with a large font
    printBig(tempMax, humMax)
    
    # Displays bitmaps
    showBitmaps()
    
    display.draw_text(0, 0, "MAX", fixed, False)

    # Update screen
    display.present()

def showAvg(values):
    # Displays average values from the last 100 measurements
    tempSum = 0
    humSum = 0
    
    for value in values:
        tempSum = tempSum + value[0]   # Temperature
        humSum  = humSum  + value[1]   # Humidity
    
    tempAvg = tempSum / len(values)
    humAvg  = humSum  / len(values)

    # Prints values with a large font
    printBig(tempAvg, humAvg)
    
    # Displays bitmaps
    showBitmaps()
    
    display.draw_text(0, 0, "AVG", fixed, False)

    # Update screen
    display.present()

def printError():
    
    display.clear()

    # Error message
    display.draw_text(0, 0, "ERROR Sensor!", fixed, False)

    # Update screen
    display.present()
    
####################  Main Code  ###################

# Create I2C object
i2c = SoftI2C(freq=400000, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN)) 

# Create display object
display = Display(i2c=i2c, width=128, height=64)

# Create sensor object
sensorTH = DHT11(Pin(DHT11_PIN))

# Create object for the User button on the board
button = Pin(D1, Pin.IN, Pin.PULL_UP)

# Load fonts
perfect = XglcdFont('fonts/PerfectPixel_23x32.c', 23, 32)
fixed   = XglcdFont('fonts/FixedFont5x8.c', 5, 8)

# Create object list to store values for the graph
listTH = deque([], maxValues)  # Does not use maxlen=


# Start by showing values
modeIndex = 0

# Reset error condition
errorFlag = False

# Loop
while (True):
        
    # Measure temperature and humidity
    try:        
        sensorTH.measure()
    
        # Separate values
        temp = sensorTH.temperature()
        hum  = sensorTH.humidity()
        
    except Exception as e:
        print(f"Error reading the sensor: {e}")
        printError()
        sleep(5)
 
        errorFlag = True
        
        continue  # Skip the following code    
    
        # Proceed if no reading error
    
    if (errorFlag == True):  # Comes from error condition
        errorFlag = False
        print("Clear!")

        display.clear()
        
    # Save to the list (deque)
    listTH.append((temp, hum))

    # Print to console
    print(temp, "degrees")
    print(hum, "%")
    
    # Change display mode if button is pressed
    if (readButton() == 0):
        beep()
        modeIndex = (modeIndex + 1) % len(modes)
        display.clear()

    # Show the active display
    if (modes[modeIndex] == "Values"):
        showTH(temp, hum)
    elif (modes[modeIndex] == "Min"):
        showMin(listTH)
    elif (modes[modeIndex] == "Max"):
        showMax(listTH)
    elif (modes[modeIndex] == "Avg"):
        showAvg(listTH)
    elif (modes[modeIndex] == "PlotTemp"):
        plotTemp(listTH)
    else:
        plotHum(listTH)
            
    # Wait for the next measurement
    sleep(sampleTime)
