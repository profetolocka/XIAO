# Uso de bitmaps en OLED

# Descripción
Este es un ejemplo de uso del OLED de la Base expansion de XIAO. Se muestra un bitmap (logo de Seeed Studio) utilizando la librería de [rdagger](https://github.com/rdagger/micropython-ssd1306)
![alt text](images/C3BaseOledDHT11Bitmaps.jpg)

# Librerías

Usa la librería https://github.com/rdagger/micropython-ssd1306/blob/main/demo_images.py y muestra el logo de Seeed Studio en pantalla

Este proyecto utiliza la librería `ssd1306.py` creada por [rdagger](https://github.com/rdagger/micropython-ssd1306). La misma ha sido incluida bajo la licencia MIT.
Hay que copiarla en la carpeta \lib de la XIAO

El código carga la imagen 'seeedLogo.mono' desde la carpeta '\images' en el sistema de archivo

Esta imagen y la original en formato BMP están en la carpeta 'images' del repositorio. En la misma carpeta se encuentra el programa img2c.py que permite convertir la imagen BMP al formato img2monoHMSB.py
Esto se hace de la siguiente forma:
(En la ventana de comandos)

python img2monoHMSB.py seeedLogo.bmp
El archivo seeedLogo.mono generado debe cargarse en la carpeta \images de la XIAO

