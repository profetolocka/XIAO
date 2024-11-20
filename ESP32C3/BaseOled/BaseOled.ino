#include <U8g2lib.h>
#include <Wire.h>

U8X8_SSD1306_128X64_NONAME_HW_I2C u8x8(/* clock=*/ SCL, /* data=*/ SDA, /* reset=*/ U8X8_PIN_NONE);   // OLEDs without Reset of the Display


void Beep (int bips) {
 
 for (int x=0; x<bips; x++) {
    digitalWrite (D3, HIGH);
    delay (1);
    digitalWrite (D3, LOW);
    delay (1);

 }

}

void setup() {
  Serial.begin(115200);

  pinMode (D3, OUTPUT);

  u8x8.begin ();
}

void loop() {

  Beep (100);
  delay (1000);

  u8g8.clearBuffer ();

    // Dibuja texto en la pantalla
  u8g2.setFont(u8g2_font_ncenB08_tr); // Selecciona una fuente
  u8g2.drawStr(0, 20, "Hola, Mundo!"); // Escribe texto en (x, y)

  // Enviar al display
  u8g2.sendBuffer();
}
