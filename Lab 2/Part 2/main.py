import time
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from datetime import datetime
from fruits_clock_image import display_image_and_text

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
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

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0

# Build Font
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

# Turn On the Backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()





from method import GetTime, ProcessTime, Timer, GetFruitImage, GetSeasonImage

fruitIndex = 0
curr_month = GetTime()
seasonIndex = ProcessTime(curr_month)
seasons = ["Winter", "Spring", "Summer", "Autumn"]
fruitdict = {"Winter": ["Pomegranate", 
                        "Pomelo", 
                        "Tangerine", 
                        "Kiwi"], 
             "Spring": ["Cherry",
                        "Persimmon",
                        "Orange",
                        "Strawberry"],
             "Summer": ["Watermelon",
                        "Peach",
                        "Grape",
                        "Lychee"],
             "Autumn": ["Cranberry",
                        "Pear",
                        "Honeydew",
                        "Mango"]}

curr_month = GetTime()
fruits = fruitdict[seasons[seasonIndex]]
fruitImage = GetFruitImage(seasons[seasonIndex], fruits[fruitIndex])
seasonImage = GetSeasonImage(seasons[seasonIndex])
text_output = Timer(curr_month, seasonIndex)
display_image_and_text(seasonImage, fruitImage, text_output)

while True:

    curr_month = GetTime()
    fruits = fruitdict[seasons[seasonIndex]]

    if buttonA.value and buttonB.value:
        continue

    # just button A pressed
    # Loops through the fruits
    
    elif not buttonA.value and buttonB.value:

        fruitIndex = (fruitIndex + 1) % len(fruits)

    # just button B pressed
    # Loops through the seasons
    elif not buttonB.value and buttonA.value:

        seasonIndex = (seasonIndex + 1) % len(seasons)
        fruits = fruitdict[seasons[seasonIndex]]
        fruitIndex = 0

    fruitImage = GetFruitImage(seasons[seasonIndex], fruits[fruitIndex])
    seasonImage = GetSeasonImage(seasons[seasonIndex])
    text_output = Timer(curr_month, seasonIndex)
    

    display_image_and_text(seasonImage, fruitImage, text_output)

    time.sleep(0.1)