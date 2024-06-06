# FeatherS3 Neo Shipping Demo
# 2024 Seon Rozenblum, Unexpected Maker
#
# Project home:
#   https://feathers3.io
#

import time, gc
from feathers3neo import FeatherS3NeoHelper, MatrixMessage, MatrixAnimation

helper = FeatherS3NeoHelper()
# Turn on the power to the NeoPixel matrix
helper.set_pixel_matrix_power(True)

# Say hello
print("\nHello from FeatherS3 Neo!")
print("-------------------------\n")

# Show available memory
print("Memory Info - gc.mem_free()")
print("---------------------------")
print(f"{gc.mem_free()} Bytes\n")

# Show flash size
# CircuitPython reserves a bunch of flash space for other features like OTA updates.
# If you would like to have access more of the 4MB of flash, you will need to compile
# your own CircuitPython firmware with a custom flash partition layout 
flash_size, flash_free = helper.flash_info
print("Flash - os.statvfs('/')")
print("---------------------------")
print(f"Partition Size: {flash_size} Bytes\nFree: {flash_free} Bytes\n")

# Get VBAT voltage
print("Approximate VBAT voltage")
print("------------------------")
print(f"{helper.battery_voltage}v\n")

# Check 5V Sense
print("Is 5V (VBUS) present?")
print("---------------------")
print(f"{helper.vbus_present}\n")

print("Pixel Time!\n")

# Create a color wheel index and a 
color_index = 0
# color time delay step
NEXT_COL = 0.01

# Initialise the matrix animation class, passing it the matrix, the animation shape name, and the trail length
# You can use this class to make pretty trail based shape animations
matrix_anim = MatrixAnimation(helper.matrix, 'spiral', 7)

# Initialise the matrix in Message mode, so you can display scrolling text on it
matrix = MatrixMessage(helper.matrix)

# Use get_characters() to build a message that shows every character in the font
# A great way to visualise al of the chars available
# message = matrix.get_characters()

message = "  Hello! "

# Set the scroll direction for the message
# valid directions are: direction LEFT, STATIC, RIGHT,
matrix.scroll_direction = matrix.LEFT

# Set the display rotation 
matrix.display_rotation = 0

# Setup the message, passing it the message, the scroll delay step in ms (default is 0.2) and if there should be padding between each character, or if they should butt up against eachother (default is True)
matrix.setup_message(message, delay=0.12, use_padding=True)

# Declare the R G B colors
r,g,b = 0,0,0

# Next colour step internal
next_color_step = 0.01

# Rainbow colors on the NeoPixel
while True:
    # Update the color from the color wheel every 10ms
    if time.monotonic() > NEXT_COL + next_color_step:
        color_index += 1
        # Get the R,G,B values of the next color
        r,g,b = helper.rgb_color_wheel( color_index )
        
        NEXT_COL = time.monotonic()

        # Set the color on the NeoPixel
        helper.pixel[0] = (r, g, b)
        
        # If the color_index is divisible by 100, flip the state of the blue LED on IO13
        if color_index % 100 == 0:
            helper.blue_led = not helper.blue_led
        
    # Show the message on the matrix if there is still something to show 
    if matrix.show_message(color=[r,g,b], brightness=0.2, fade_out=0.2):
        # We don't need to do anything here
        pass
    else:
        # Animate the RGB Matrix with the animation setup above
        matrix_anim.animate(r, g, b)
        # Sleep for 40ms so the animation cycle isn't too fast
        time.sleep(0.04)

