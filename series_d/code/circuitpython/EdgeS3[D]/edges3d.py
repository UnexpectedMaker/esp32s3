# EdgeS3[D] Helper Library
# 2025 Seon Rozenblum, Unexpected Maker
#
# Project home:
#   https://edges3.io
#

# Import required libraries
import time
import board, microcontroller
import adafruit_max1704x
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn

# Setup the RF switch pin
ant_selection = DigitalInOut(microcontroller.pin.GPIO38)
ant_selection.direction = Direction.OUTPUT

i2c = board.I2C()  # uses board.SCL and board.SDA
max17 = adafruit_max1704x.MAX17048(i2c)


# Helper functions
def set_antenna_external( state ):
    """Set the RF switch to the external uFL connector."""
    ant_selection.value = state

def get_battery_voltage():
    """Get the approximate battery voltage."""
    return max17.cell_voltage

def get_battery_percentage():
    """Get the approximate battery percentage."""
    return max17.cell_percent
    

