# Code - Unexpected Maker - Series[D] Boards 
Code examples, shipping files and helper libraries for Series[D] boards

Currently includes:

## CircuitPython
Shipping files includes the Circ uitPython helper library and code.py, for each board, plus a `lib` folder populated with the requirements for the `Adafruit MAX17048` Battery FG IC library.

CircuitPython support for EdgeS3[D] (that the EdgeS3[D] ships with) has been PR'd and merged into the CircuiPython repo for a future release.

There are no Series[D] board specific CircuitPython builds for TinyS3[D], ProS3[D] and FeatherS3[D] - They use their origional non Series[D] board CircuitPython builds.

Due to this, not every IO used on a Series[D] board is available in the `boards` import, but all IO can be accessed using `microcontroller.pin`, for example, to access IO11 on the ProS3 buildind running on the ProS3[D], you use the following syntax:

``` python
# Setup the RF switch pin
ant_selection = DigitalInOut(microcontroller.pin.GPIO11)
ant_selection.direction = Direction.OUTPUT
```

## MicroPython
MicroPython builds for TinyS3[D], ProS3[D] and FeatherS3[D] use the origional TinyS3, ProS3 and FeatherS3 builds available at [micropython.org](https://micropython.org/download/?vendor=Unexpected%20Maker)

Helper libraries and example code wil be available soon.

## Arduino
Check the Arduino folder for a link to the Series[D] Helper library and example code for the Arduino IDE, to be installed via the library manager 

## PlatformIO
Soon!

You can find out more about my Series[D] boards at https://esp32s3.com 

Please refer to the included license. 
