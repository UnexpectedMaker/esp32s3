# Unexpected Maker ESP32-S3 Arduino Helper Library

This is the [helper library](https://github.com/UnexpectedMaker/seriesd_arduino_helper) for all the Unexpected Maker [Series[D] boards](https://esp32s3.com).

Examples can be found in the [examples directory](https://github.com/UnexpectedMaker/seriesd_arduino_helper/tree/main/examples), these can also be loaded from the examples menu in the Arduino IDE.

Examples include switching ANtenna output, Reading the battery, controlling the RGB LED (if one is present on the board)

## Installation

Please download the library called `UM Series[D] Helper` via the Arduino Library Manager.

## List of functions

```c++

// Initializes all UM Series[D] board peripherals
void begin();

// Set LDO2 on or off
// Only available on the ProS3[D] and FeatherS3[D] 
void setLDO2Power(bool on);

// Set RGB LED power on or off (On ProS3[D] and FeatherS3[D] it sets LDO2 on)
// Not available on the EdgeS3[D] 
void setPixelPower(bool on);

// Set RGB LED color
// Not available on the EdgeS3[D] 
void setPixelColor(uint8_t r, uint8_t g, uint8_t b);
void setPixelColor(uint32_t rgb);

// Set RGB LED brightness
// Not available on the EdgeS3[D] 
void setPixelBrightness(uint8_t brightness);

// Pack r,g,b (0-255) into a 32bit rgb color
static uint32_t color(uint8_t r, uint8_t g, uint8_t b);

// Convert a color wheel angle (0-255) to a 32bit rgb color
static uint32_t colorWheel(uint8_t pos);

// Set the blue LED on or off
// Only available on the FeatherS3[D]
void setBlueLED(bool on);

// Get the light sensor in volts (0-3.3)
// Only available on the FeatherS3[D]
float getLightSensorVoltage();

// Toggle the blue LED
// Only available on the FeatherS3[D]
void toggleBlueLED();

// Get the battery voltage in volts
// This function gets the voltage from the MAX17048
float getBatteryVoltage();

// Detect if VBUS (USB power) is present
// Not available on the EdgeS3[D] 
bool getVbusPresent();

// Set the RF Switch to external antenna
void setAntennaExternal(bool state);
```
