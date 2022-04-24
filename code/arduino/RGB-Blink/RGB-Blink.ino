#include <FastLED.h>

// How many leds in your strip?
#define NUM_LEDS 1

#define DATA_PIN 18
#define POWER_PIN 17

// Define the array of leds
CRGB leds[NUM_LEDS];

void setup() { 

  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);  // GRB ordering is assumed

  // Enable LED
  pinMode(POWER_PIN, OUTPUT);
  digitalWrite(POWER_PIN, HIGH);
}

void loop() { 
  // Turn the LED on, then pause
  leds[0] = CRGB::Green;
  FastLED.show();
  delay(500);

  // Now turn the LED off, then pause
  leds[0] = CRGB::Black;
  FastLED.show();
  delay(500);
}
