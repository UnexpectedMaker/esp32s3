# FeatherS3 Neo Helper Library
# 2024 Seon Rozenblum, Unexpected Maker
#
# Project home:
#   https://feathers3.io
#

# Import required libraries
import time
import neopixel
import board
from os import statvfs
from micropython import const
from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn

class FeatherS3NeoHelper:
	def __init__(self):
		# pin 13 and on-board RGB
		self._led13 = DigitalInOut(board.LED)
		self._led13.direction = Direction.OUTPUT
		
		# Setup the NeoPixel power pins
		self._pixel_power = DigitalInOut(board.NEOPIXEL_POWER)
		self._pixel_power.direction = Direction.OUTPUT
		self._pixel_power.value = True

		# Setup the BATTERY voltage sense pin
		self._vbat_voltage = AnalogIn(board.BATTERY)

		# Setup the VBUS sense pin
		self._vbus_sense = DigitalInOut(board.VBUS_SENSE)
		self._vbus_sense.direction = Direction.INPUT
		
		# Create a NeoPixel reference
		self._pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=0.3, auto_write=True, pixel_order=neopixel.RGB)

		# Create a NeoPixel matrix reference
		self._matrix = neopixel.NeoPixel(board.NEOPIXEL_MATRIX, 49, brightness=0.3, auto_write=True, pixel_order=neopixel.RGB)
		
		# Initially set the matrix power off
		self._pixel_power.value = False
	

	def set_pixel_matrix_power(self, state):
		"""Enable or Disable power to the onboard NeoPixel to either show colour, or to reduce power fro deep sleep"""
		self._pixel_power.value = state
	
	def get_battery_voltage(self):
		"""Get the approximate battery voltage"""
		# I don't really understand what CP is doing under the hood here for the ADC range & calibration,
		# but the onboard voltage divider for VBAT sense is setup to deliver 1.1V to the ADC based on it's
		# default factory configuration.
		# This forumla should show the nominal 4.2V max capacity (approximately) when 5V is present and the
		# VBAT is in charge state for a 1S LiPo battery with a max capacity of 4.2V   
		return round(self._vbat_voltage.value / 5370,2)

	def get_vbus_present(self):
		"""Detect if VBUS (5V) power source is present"""
		return self._vbus_sense.value
	
	def get_flash_info(self):
		flash = statvfs('/')
		flash_size = flash[0] * flash[2]
		flash_free = flash[0] * flash[3]
		return flash_size, flash_free
	
	@staticmethod
	def rgb_color_wheel(wheel_pos):
		"""Color wheel to allow for cycling through the rainbow of RGB colors."""
		wheel_pos = wheel_pos % 255

		if wheel_pos < 85:
			return 255 - wheel_pos * 3, 0, wheel_pos * 3
		elif wheel_pos < 170:
			wheel_pos -= 85
			return 0, wheel_pos * 3, 255 - wheel_pos * 3
		else:
			wheel_pos -= 170
			return wheel_pos * 3, 255 - wheel_pos * 3, 0
		
	@property
	def battery_voltage(self):
		return self.get_battery_voltage()
	
	@property
	def vbus_present(self):
		return self.get_vbus_present()
	
	@property
	def pixel(self):
		return self._pixel
	
	@property
	def matrix(self):
		return self._matrix
	
	@property
	def flash_info(self):
		return self.get_flash_info()
	
	@property
	def blue_led(self):
		return self._led13.value
	
	@blue_led.setter
	def blue_led(self,value):
		# Turn the Blue LED on or off
		self._led13.value = value
	

class MatrixMessage:
	
	STATIC = const(0)
	LEFT = const(1)
	RIGHT = const(2)

	def __init__(self, matrix):
		
		self.matrix = matrix
		self._message_width = 0
		self._message_index = 0
		self._pixel_data = []
		self._scroll_direction = MatrixMessage.LEFT
		self.current_rotation = 0
		self._scroll_delay = 0.15
		self._pixel_data_length = 0
		self._next_tick = 0
		
		self.glyphs = {
			" ": [0,0,0,0,0],
			"!": [0,29,0,0,0],
			"\"": [0,24,0,24,0],
			"#": [10,31,10,31,10],
			"$": [10,29,21,23,10],
			"%": [25,18,4,9,19],
			"&": [10,21,21,10,1],
			"'": [0,24,0,0,0],
			"(": [0,14,17,0,0],
			")": [0,17,14,0,0],
			"*": [0,10,4,10,0],
			"+": [0,4,14,4,0],
			",": [0,1,2,0,0],
			"-": [0,4,4,4,0],
			".": [0,2,0,0,0],
			"/": [1,2,4,8,16],
			"0": [14,17,17,14,0],
			"1": [0,9,31,1,0],
			"2": [19,21,21,9,0],
			"3": [18,17,21,26,0],
			"4": [6,10,18,31,2],
			"5": [29,21,21,21,18],
			"6": [2,5,13,21,2],
			"7": [17,18,20,24,16],
			"8": [10,21,21,21,10],
			"9": [8,21,22,20,8],
			":": [0,10,0,0,0],
			";": [0,1,10,0,0],
			"<": [0,4,10,17,0],
			"=": [0,10,10,10,0],
			">": [0,17,10,4,0],
			"?": [8,16,21,20,8],
			"@": [14,17,21,18,14],
			"A": [15,20,20,15,0],
			"B": [31,21,21,10,0],
			"C": [14,17,17,17,0],
			"D": [31,17,17,14,0],
			"E": [31,21,21,17,0],
			"F": [31,20,20,16,0],
			"G": [14,17,17,21,6],
			"H": [31,4,4,31,0],
			"I": [17,31,17,0,0],
			"J": [18,17,17,30,16],
			"K": [31,4,10,17,0],
			"L": [31,1,1,1,0],
			"M": [31,8,4,8,31],
			"N": [31,8,4,2,31],
			"O": [14,17,17,14,0],
			"P": [31,20,20,8,0],
			"Q": [12,18,19,13,0],
			"R": [31,20,20,10,1],
			"S": [9,21,21,18,0],
			"T": [16,16,31,16,16],
			"U": [30,1,1,30,0],
			"V": [28,2,1,2,28],
			"W": [31,2,4,2,31],
			"X": [27,4,4,27,0],
			"Y": [16,8,7,8,16],
			"Z": [19,21,25,17,0],
			"[": [0,31,17,17,0],
			"\\": [16,8,4,2,1],
			"]": [0,17,17,31,0],
			"^": [0,8,16,8,0],
			"_": [1,1,1,1,1],
			"`": [0,16,8,0,0],
			"a": [6,9,9,15,1],
			"b": [31,5,5,2,0],
			"c": [6,9,9,9,0],
			"d": [2,5,5,31,0],
			"e": [14,21,21,9,0],
			"f": [4,15,20,16,0],
			"g": [8,21,21,30,0],
			"h": [31,4,4,3,0],
			"i": [0,23,0,0,0],
			"j": [0,1,1,22,0],
			"k": [31,4,10,1,0],
			"l": [0,30,1,1,0],
			"m": [15,8,4,8,15],
			"n": [15,8,8,7,0],
			"o": [6,9,9,6,0],
			"p": [15,10,10,4,0],
			"q": [4,10,10,15,0],
			"r": [7,8,8,8,0],
			"s": [1,5,10,8,0],
			"t": [0,30,5,5,1],
			"u": [14,1,1,15,1],
			"v": [12,2,1,2,12],
			"w": [15,1,2,1,15],
			"x": [9,6,6,9,0],
			"y": [9,5,2,4,8],
			"z": [9,11,13,9,0],
			"{": [0,4,31,17,0],
			"|": [0,31,0,0,0],
			"}": [17,31,4,0,0],
			"~": [0,4,4,2,2],
			'↑': [4,8,31,8,4],
			'→': [4,4,21,14,4],
			'↓': [4,2,31,2,4],
			'←': [4,14,21,4,4],
			'▲': [2, 6, 14, 6, 2],
			'►': [0, 31, 14, 4, 0],
			'▼': [8, 12, 14, 12, 8],
			'◄': [0, 4, 14, 31, 0],
			"☐": [0, 14, 10, 14, 0],
			"□": [31, 17, 17, 17, 31],
			"℃": [24, 24, 7, 5, 5],
			"℉": [24, 24, 7, 6, 4],
			'π': [16, 31, 16, 31, 17],
			'å': [6,9,27,15,1],
			
		}
		
		self.wifi_anim = [
			[1, 0, 0, 0, 0],
			[5, 4, 3, 0, 0],
			[21, 20, 19, 8, 7]
		]
		
	def get_characters(self):
		return f"{''.join(sorted(self.glyphs.keys()))} " 
	
	def get_character(self, c):
		if c not in self.glyphs:
			print(f"{c} not in font glyphs, sorry!")
			return None
		
		glyph_data = self.glyphs[c]
		bits = [0] * 25
		bit = 0
		for x in range(5):
			for y in range(5):
				v = (glyph_data[x] >> (4-y)) & 1
				bits[bit] = v
				bit+=1
				
		return bits
	
	def get_message_width(self, txt, use_padding = True):
		total_width = 0
		for i, c in enumerate(txt):
			# Special case for space
			width = 0
			if c == " ":
				width = 2
			elif c in self.glyphs:
				glyph_data = self.glyphs[c]
				for x in range(5):
					width += 1 if glyph_data[x] > 0 else 0

			# Extra 1 to ensure 1 colum padding for every character in the string
			total_width += (width + 1) if use_padding else width
			
		return total_width
				
	
	def get_message(self, txt, use_padding = True):
		
		width = self.get_message_width(txt, use_padding)
		# print(f"width: {width}")
		bits = [0] * (width * 7)
		# print(f"len bits {len(bits)}")
		bit = 0
		for i, c in enumerate(txt):
			# Special case for space
			if c == " ":
				bit+= 14
			elif c in self.glyphs:
				glyph_data = self.glyphs[c]
				for x in range(5):
					if glyph_data[x] > 0:
						for y in range(7):
							if y < 5:
								v = (glyph_data[x] >> (4-y)) & 1
								bits[bit] = v
							else:
								bits[bit] = 0
							bit+= 1
			if use_padding:
				bit+= 7
		
		return width, bits
	
	def setup_message(self, message, delay=0.2, use_padding=True):
		""" setup the message
			message:        The message to display
			delay:          The scroll speed delay step in ms
			use_padding:    If there should be padding between each character
		"""
		self._scroll_delay = delay
		self._message = message
		self._message_width, self._pixel_data = self.get_message(message, use_padding)
		self._pixel_data_length = len(self._pixel_data )
		self._next_tick = time.monotonic()
		self._fade = 1
		# Set the current index to the start or end depending on direction
		self._message_index = self._message_width if self._scroll_direction == MatrixMessage.RIGHT else 0
		
	def show_message(self, color, brightness = 0.33, fade_out=0.2):
		""" show the message on the matrix
			color:      The r,g,b colour each visible LED should be this update
			brightness: Multiplier for the color as the neopixel lib doesn't have a brightness setting
			fade_out:   fade step for each character being show. Only use when display messages in STATIC movement mode
						to help reduce transition shock and to separate showing identical characters consecutively 
		"""
		if self._scroll_direction == MatrixMessage.LEFT and self._message_index >= self._message_width:
			return False
		elif self._scroll_direction == MatrixMessage.RIGHT and self._message_index <= 0:
			return False
		elif self._scroll_direction == MatrixMessage.STATIC and self._message_index >= len(self._message)-1:
			return False

		if time.monotonic() > self._next_tick + self._scroll_delay:
			self._next_tick = time.monotonic()
			# Adjust index based on scroll direction
			self._message_index += -1 if self._scroll_direction == MatrixMessage.RIGHT else 1
			self._fade = 1

		if self._scroll_direction == MatrixMessage.STATIC:
			brightness *= self._fade
			self._fade = max(self._fade - fade_out, 0)

		col_on = [c * brightness for c in color ]
		col_off = [0,0,0]

		if self._scroll_direction == MatrixMessage.STATIC:
			for led, p in enumerate(self.get_character(self._message[self._message_index])):
				self.matrix[led] = col_on if p else col_off
			return True
		
		# Hacky transposing of the message data because FeatherS2 neo have column layout for matrix and FeatherS3 neo has row layout for matrix. Silly Seon!
		_x = 0
		_y = 0
		_new_led = 0
		for led in range(49):
			index = led + 7 * self._message_index
			if index < self._pixel_data_length:
				self.matrix[_new_led] = col_on if self._pixel_data[index] else col_off
				_y += 1
				if _y > 6:
					_x += 1
					_y = 0
				_new_led = _x + _y * 7
				
				
		return True
				
	@property
	def scroll_direction(self):
		return self.scroll_direction
	
	@scroll_direction.setter
	def scroll_direction(self,value):
		# Set the scroll direction
		self._scroll_direction = value
		
	@property
	def display_rotation(self):
		return self.current_rotation
	
	@display_rotation.setter
	def display_rotation(self,value):
		# Set the scroll direction
		self.current_rotation = value

class MatrixAnimation:
	
	def __init__(self, matrix, anim_type, trail_length):
		
		# List of animation shapes by pixel index
		# Pixel 0 is Top Left, pixels increase vertically by row
		# Feel free to make your own shapes!   
		self.matrix_display_shapes = {
			"square": [0,1,2,3,4,5,6,13,20,27,34,41,48,47,46,45,44,43,42,35,28,21,14,7],
   			"spiral": [24,25,32,31,30,23,16,17,18,25,32,39,38,37,36,29,22,15,8,9,10,11,12,19,26,33,40,47,46,45,44,43,42,35,28,21,14,7,0,1,2,3,4,5,6,13,20,27,34,41,48,47,46,45,44,43,42,35,28,21,14,7,8,9,10,11,12,19,26,33,40,39,38,37,36,29,22,15,16,17,18,25,32,31,30,23,24,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
		}
			
		# Initialiation error status
		self.error = False
		
		if anim_type not in self.matrix_display_shapes:
			print(f"** '{anim_type}' not found in list of shapes!\n** Animation halted!")
			self.error = True
		elif trail_length < 1 or trail_length > 20:
			print(f"** trail_length cannot be {trail_length}. Please pick a value between 1 and 20!\n** Animation halted!")
			self.error = True
		
		if not self.error: 
			self.matrix = matrix
			self.anim_type = anim_type
			self.trail_length = trail_length + 1
			
			# Create the trail list base don the length of the trail
			self.anim_trail = [x for x in range(0, -self.trail_length,-1)]
			
			# Create a reference to the selected animation list
			self.current_anim = self.matrix_display_shapes[self.anim_type]

	def get_alpha(self):
		return 0.2 * (self.trail_length-1)
	
	def inc_anim_index(self, index):
		self.anim_trail[index] += 1
		if self.anim_trail[index] == len(self.current_anim):
			self.anim_trail[index] = 0
	
	def get_anim_index(self, index ):
		return self.current_anim[self.anim_trail[index]]
	
	def animate(self, r, g, b):
		if not self.error:             
			alpha = self.get_alpha()
			for index in range(self.trail_length):
				if self.anim_trail[index] > -1:
					(r2, g2, b2) = r * alpha, g * alpha, b * alpha
					if self.get_anim_index(index) > -1:
						self.matrix[ self.get_anim_index(index) ] = (r2, g2, b2)
					alpha = alpha - 0.2 if alpha > 0.2 else 0
				
				self.inc_anim_index(index)
				
class MatrixDigitalScope:
	def __init__(self, pin):
		self.pin = pin
		
	def get_pin(self, col):
		# print(self.pin.value)
		if self.pin.value:
			return 0
		else:
			return 4
	