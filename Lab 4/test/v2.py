from __future__ import print_function
import qwiic_button
import qwiic_joystick
import time
import sys
import random
import board
import busio
import adafruit_mpr121
import adafruit_rgb_display.st7789 as st7789
from PIL import Image, ImageDraw, ImageFont
import threading
import digitalio
import json

buttons = [None] * 8
joystick = None
delay = 0.05
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)
score = 0
global_end = False

disp = st7789.ST7789(
    board.SPI(),
    cs=digitalio.DigitalInOut(board.CE0),
    dc=digitalio.DigitalInOut(board.D25),
    rst=None,
    baudrate=64000000,
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

def init_buttons():

  buttons[0] = qwiic_button.QwiicButton(0x6F)
  buttons[1] = qwiic_button.QwiicButton(0x6E)
  buttons[2] = qwiic_button.QwiicButton(0x6D)
  buttons[3] = qwiic_button.QwiicButton(0x6C)
  buttons[4] = qwiic_button.QwiicButton(0x6B)
  buttons[5] = qwiic_button.QwiicButton(0x6A)
  buttons[6] = qwiic_button.QwiicButton(0x69)
  buttons[7] = qwiic_button.QwiicButton(0x68)

  for i in range(8):
    if buttons[i].begin() == False:
      print(f"BUTTON {i} NOT CONNECTED")

  return buttons

def init_joystick():

  joystick = qwiic_joystick.QwiicJoystick()
  joystick.begin()
  return joystick

def flash(index):

  for _ in range(3):
    try: buttons[index].LED_on(100)
    except: pass
    time.sleep(0.02)
    try: buttons[index].LED_off()
    except: pass
    time.sleep(0.02)

def end():

  global global_end
  global_end = True
  time.sleep(1)

  for i in range(8):
    try: buttons[i].LED_off()
    except: pass
    time.sleep(0.02)

  high_score = 0

  with open("./scores.json", 'r+') as f:
    data = json.load(f)

  if data["high_score"] < score:
    high_score = data["high_score"]
    data["high_score"] = score
  else:
    high_score = data["high_score"]

  with open("./scores.json", 'w') as f:    
    f.seek(0)
    json.dump(data, f, indent=2)
    f.truncate()
    f.close()

  # Draw a black filled box to clear the image.
  draw.rectangle((0, 0, width, height), outline=0, fill=0)

  y = top
  if score > high_score:
    draw.text((0,y), f"High Score: {score}", font=font, end="", flush=True, fill="#FFFFFF")
    y += 24
    draw.text((0,y), f"GAME OVER", font=font, end="", flush=True, fill="#FFFFFF")
    y += 24
    draw.text((0,y), f"NEW HIGH SCORE!", font=font, end="", flush=True, fill="#FFFFFF")
  else:
    draw.text((0,y), f"High Score: {high_score}", font=font, end="", flush=True, fill="#FFFFFF")
    y += 24
    draw.text((0,y), f"GAME OVER", font=font, end="", flush=True, fill="#FFFFFF")
    y += 24
    draw.text((0,y), f"HAHA YOU LOST :D", font=font, end="", flush=True, fill="#FFFFFF")

  y += 24
  draw.text((0,y), f"Score: {score}", font=font, end="", flush=True, fill="#FFFFFF")

  # Display image.
  disp.image(image, rotation)
  time.sleep(0.01)

  for i in range(4):
    for i in range(8):
      try: buttons[i].LED_off()
      except: pass
      time.sleep(0.02)

    for i in range(8):
      try: buttons[i].LED_on(100)
      except: pass
      time.sleep(0.02)

  exit(1)

if __name__ == '__main__':

  try:

    buttons = init_buttons()
    joystick = init_joystick()

  except (KeyboardInterrupt, SystemExit) as exErr:

    sys.exit(0)

  for i in range(8):
    buttons[i].LED_off()

  mole = random.randrange(1,8,2)
  hit = False
  timer = threading.Timer(20, end)

  for i in range(8):
    try: buttons[i].LED_on(100)
    except: pass
    time.sleep(0.05)

  for i in range(8):
    try: buttons[i].LED_off()
    except: pass
    time.sleep(0.05)

  time.sleep(1)
  buttons[mole].LED_on(100)
  timer.start()

  while True:
  
    if global_end:
      exit(1)

    button_hit = mpr121[0].value
  
    if hit == True:
      mole = random.randrange(1,8,2)
      buttons[mole].LED_on(100)  
      hit = False
      score += 1

    x = joystick.horizontal - 505
    y = joystick.vertical - 504

    if x < 0 and y < 0:
      try: buttons[6].LED_on(100)
      except: pass
      time.sleep(0.05)
      if mole == 7 and button_hit:
        try: buttons[mole].LED_off()
        except: pass
        hit = True
        flash(mole)

    elif x > 0 and y < 0:
      try: buttons[4].LED_on(100)
      except: pass
      time.sleep(0.05)
      if mole == 5 and button_hit:
        try: buttons[mole].LED_off()
        except: pass
        hit = True
        flash(mole)

    elif x < 0 and y > 0:
      try: buttons[2].LED_on(100)
      except: pass
      time.sleep(0.05)
      if mole == 3 and button_hit:
        try: buttons[mole].LED_off()
        except: pass
        hit = True
        flash(mole)

    elif x > 0 and y > 0:
      try: buttons[0].LED_on(100)
      except: pass
      time.sleep(0.05)
      if mole == 1 and button_hit:
        try: buttons[mole].LED_off()
        except: pass
        hit = True
        flash(mole)

    else:
      for i in [0,2,4,6]:
        try: buttons[i].LED_off()
        except: pass
        time.sleep(0.05)
