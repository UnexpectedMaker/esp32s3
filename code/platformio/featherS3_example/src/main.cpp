#include <UMS3.h>

UMS3 ums3;

uint32_t led_cycle_count = 0;

void setup() {
  Serial.begin(115200);

  // Initialize all board peripherals, call this first
  ums3.begin();

  // Brightness is 0-255. We set it to 1/3 brightness here
  ums3.setPixelBrightness(255 / 3);

  // Enable the power to the RGB LED.
  // Off by default so it doesn't use current when the LED is not required.
  ums3.setPixelPower(true);
}

int color = 0;

void loop() {
  // colorWheel cycles red, orange, ..., back to red at 256
  ums3.setPixelColor(UMS3::colorWheel(color));
  color++;

  // On the feathers3, toggle the LED twice per cycle
#ifdef ARDUINO_FEATHERS3
  if (color % 128 == 0) {
    ums3.toggleBlueLED();
  }
#endif

  if (color % 255 == 0) {
    Serial.printf("LED cycle #%d\n", ++led_cycle_count);
  }

  delay(15);
}