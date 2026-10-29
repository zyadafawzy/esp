#include <Arduino.h>
#include <SPI.h>
#include <TFT_eSPI.h>
#include <XPT2046_Touchscreen.h>
#include "images_data.h"

// دبابيس اللمس في بورد CYD (ناقل SPI منفصل عن الشاشة)
#define T_CS   33
#define T_IRQ  36
#define T_CLK  25
#define T_MOSI 32
#define T_MISO 39

TFT_eSPI tft;
SPIClass touchSPI(VSPI);
XPT2046_Touchscreen ts(T_CS, T_IRQ);

int current = 0;
bool wasTouched = false;
uint32_t lastChange = 0;

void show(int i) {
  tft.pushImage(0, 0, IMG_W, IMG_H, (uint16_t*)IMAGES[i]);
}

void setup() {
  pinMode(TFT_BL, OUTPUT);
  digitalWrite(TFT_BL, HIGH);

  tft.init();
#ifdef INVERT_COLORS
  tft.invertDisplay(true);
#endif
  tft.setRotation(1);        // عرضي 320x240
  tft.setSwapBytes(true);
  tft.fillScreen(TFT_BLACK);

  touchSPI.begin(T_CLK, T_MISO, T_MOSI, T_CS);
  ts.begin(touchSPI);
  ts.setRotation(1);

  show(0);
}

void loop() {
  bool touched = ts.tirqTouched() && ts.touched();
  if (touched && !wasTouched && millis() - lastChange > 300) {
    current = (current + 1) % IMAGE_COUNT;
    show(current);
    lastChange = millis();
  }
  wasTouched = touched;
  delay(10);
}
