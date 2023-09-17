import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.ili9341 as ili9341
import adafruit_rgb_display.st7789 as st7789  # pylint: disable=unused-import
import adafruit_rgb_display.hx8357 as hx8357  # pylint: disable=unused-import
import adafruit_rgb_display.st7735 as st7735  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1351 as ssd1351  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1331 as ssd1331  # pylint: disable=unused-import

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = digitalio.DigitalInOut(board.D24)

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

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
    rotation=90
)

if disp.rotation % 180 == 90:
    height = disp.width  # we swap height/width to rotate it to landscape!
    width = disp.height
else:
    width = disp.width  # we swap height/width to rotate it to landscape!
    height = disp.height


def display_image_and_text(background_file, fruit_file, text):
    # Create blank image for drawing.
    image = Image.new("RGB", (width, height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    disp.image(image)

    image = Image.open(background_file)
    backlight = digitalio.DigitalInOut(board.D22)
    backlight.switch_to_output()
    backlight.value = True

    # Scaling, cropping and displaying background image
    # ... (rest of the code for handling the background image)

    fruit_image = Image.open(fruit_file)

    # Processing and displaying fruit image
    fruit_image = fruit_image.convert("RGBA")

    # Make the background transparent
    data = fruit_image.getdata()
    new_data = []
    for item in data:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:  # If the item is white
            new_data.append((255, 255, 255, 0))  # Set its alpha to 0 (fully transparent)
        else:
            new_data.append(item)
    fruit_image.putdata(new_data)

    # Resize the fruit_image to 40x40
    desired_size = (50, 50)
    fruit_image = fruit_image.resize(desired_size)

    # Calculate the position to center the resized fruit_image on the main image
    x_position = (width - fruit_image.width) // 2
    y_position = (height - fruit_image.height) // 2

    # Place the resized image on the main image at the calculated position with transparency handling
    image.paste(fruit_image, (x_position+5, y_position+30), fruit_image)

    # Drawing the provided text at the center of the image
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 10)
    # Drawing the provided text at the center of the image
    draw = ImageDraw.Draw(image)  # Create a new ImageDraw object for the combined image
    # text_width, text_height = draw.textsize(text, font=font)
    text_x = 60
    text_y = 2
    draw.text((text_x, text_y), text, font=font, fill="white")


    # Display the combined image
    disp.image(image)

