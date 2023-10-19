from __future__ import print_function
import qwiic_keypad
import time
import sys
from PIL import Image, ImageDraw, ImageSequence
import digitalio
import board
import adafruit_rgb_display.st7789 as st7789

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the display:
disp = st7789.ST7789(
	spi,
	cs=cs_pin,
	dc=dc_pin,
	rst=reset_pin,
	baudrate=BAUDRATE,
	width=135,
	height=240,
	x_offset=53,
	y_offset=40,
)

# Determine the image dimensions based on display rotation
if disp.rotation % 180 == 90:
	height = disp.width
	width = disp.height
else:
	width = disp.width
	height = disp.height


continue_animation = True

def display_gif_on_rgb(gif_path, duration=0.1):
    """Display an animated GIF on the RGB display."""
    gif = Image.open(gif_path)
    frames = [frame.copy().convert("RGB") for frame in ImageSequence.Iterator(gif)]

    try:
        while True:  # Loop to keep the GIF playing continuously
            for frame in frames:
                # Scale the image to the smaller screen dimension
                image_ratio = frame.width / frame.height
                screen_ratio = width / height
                if screen_ratio < image_ratio:
                    scaled_width = frame.width * height // frame.height
                    scaled_height = height
                else:
                    scaled_width = width
                    scaled_height = frame.height * width // frame.width
                frame = frame.resize((scaled_width, scaled_height), Image.BICUBIC)

                # Crop and center the image
                x = scaled_width // 2 - width // 2
                y = scaled_height // 2 - height // 2
                frame = frame.crop((x, y, x + width, y + height))

                # Display the frame
                disp.image(frame)
                time.sleep(duration)  # Pause for the duration of the frame
    except KeyboardInterrupt:
        pass  # Allow the user to stop the GIF playback with a keyboard interrupt

def runExample():
	global continue_animation
	print("\nSparkFun qwiic Keypad   Example 1\n")
	myKeypad = qwiic_keypad.QwiicKeypad()

	if myKeypad.connected == False:
		print("The Qwiic Keypad device isn't connected to the system. Please check your connection", \
			file=sys.stderr)
		return

	myKeypad.begin()

	print("Initialized. Firmware Version: %s" % myKeypad.version)
	print("Press a button: * to do a space. # to go to next line.")

	button = 0
	try:
		while True:
			myKeypad.update_fifo()  
			button = myKeypad.get_button()

			if button == -1:
				print("No keypad detected")
				time.sleep(1)

			elif button != 0:
				charButton = chr(button)
				if charButton == '*':  # Start GIF animation
					display_gif_on_rgb("sirilower.gif")
				elif charButton == '#':  # Stop GIF animation
					continue_animation = False
				else: 
					print(charButton, end="")

				sys.stdout.flush()

			time.sleep(.25)
	except KeyboardInterrupt:
		continue_animation = False  # Set the flag to False when ^C is pressed

if __name__ == '__main__':
	try:
		runExample()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)
