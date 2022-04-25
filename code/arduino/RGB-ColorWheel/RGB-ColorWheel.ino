/***************************************************
 * 
 *  Rainbow Color Wheel sample using FastLED library
 *  by Sukesh Ashok Kumar
 * 
 ***************************************************/
#include <FastLED.h>

#define TINY_S3
//#define FEATHER_S3
//#define PRO_S3

#ifdef TINY_S3
  #define DATA_PIN 18
  #define POWER_PIN 17
#endif

#ifdef FEATHER_S3
  #define DATA_PIN 40
  //#define POWER_PIN 17
#endif

#ifdef PRO_S3
  #define DATA_PIN 18
  //#define POWER_PIN 17
#endif


// How many leds in your strip?
#define NUM_LEDS 1

// Define the array of leds
CRGB leds[NUM_LEDS];

#define BRIGHTNESS 100

int color_index = 0;

void setup() { 

  FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);  // GRB ordering is assumed

#ifdef TINY_S3
  // Enable LED
  pinMode(POWER_PIN, OUTPUT);
  digitalWrite(POWER_PIN, HIGH);
#endif

  FastLED.setBrightness(BRIGHTNESS);
  
}

int wr=0,wg=0,wb=0;
void loop() { 
  
  // Get the color, then pause
  rgb_color_wheel(color_index,&wr,&wg,&wb);
  
  leds[0].r = wr;
  leds[0].g = wg;
  leds[0].b = wb;

  color_index++;
  FastLED.show();
  delay(20);
}

// NeoPixel rainbow colour wheel - adapted from python sample
void rgb_color_wheel(int wheel_pos, int *r, int *g, int *b)
{
  wheel_pos = wheel_pos % 255;

  if (wheel_pos < 85)
  {
      *r = 255 - wheel_pos * 3;
      *g = 0;
      *b = wheel_pos * 3;
  }
  else if (wheel_pos < 170)
  {
        wheel_pos -= 85;
        *r = 0;
        *g = wheel_pos * 3;
        *b = 255 - wheel_pos * 3;
  }
  else
  {
        wheel_pos -= 170;
        *r = wheel_pos * 3;
        *g = 255 - wheel_pos * 3;
        *b = 0;
  }
}
