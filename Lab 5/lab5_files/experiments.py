import random
from teachable_machine_lite import TeachableMachineLite
import cv2 as cv
import pygame  # Import the pygame library

import threading

# import time
# import digitalio
# import board
# from PIL import Image, ImageDraw, ImageFont
# import adafruit_rgb_display.st7789 as st7789
# from datetime import datetime

# disp = st7789.ST7789(
#     board.SPI(),
#     cs=digitalio.DigitalInOut(board.CE0),
#     dc=digitalio.DigitalInOut(board.D25),
#     rst=None,
#     baudrate=64000000,
#     width=135,
#     height=240,
#     x_offset=53,
#     y_offset=40,
# )

# height = disp.width
# width = disp.height
# image = Image.new("RGB", (width, height))
# rotation = 90
# draw = ImageDraw.Draw(image)

# draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
# disp.image(image, rotation)

# top = -2
# bottom = height - -2
# x = 0

# font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

# backlight = digitalio.DigitalInOut(board.D22)
# backlight.switch_to_output()
# backlight.value = True

# def displayImage(file):
#     display_image = Image.open(file)
#     display_image = display_image.convert("RGBA")

#     disp.image(display_image, rotation)

# Initialize Pygame's mixer module
pygame.mixer.init()

# Dictionary of sounds for each result ID
sounds_for_id = {
    0: ['sound_effects/goose/1.mp3'],
    1: ['sound_effects/cat/1.mp3', 'sound_effects/cat/2.mp3', 'sound_effects/cat/3.mp3'],
    2: ['sound_effects/human/1.mp3']
}

cap = cv.VideoCapture(0)

model_path = 'models/model.tflite'
labels_path = "models/labels.txt"
image_file_name = "frame.jpg"

tm_model = TeachableMachineLite(model_path=model_path, labels_file_path=labels_path)
previous_id = None

def goose():
  sound_path = random.choice(sounds_for_id[0])
  sound = pygame.mixer.Sound(sound_path)
  sound.play()

def cat():
  sound_path = random.choice(sounds_for_id[1])
  sound = pygame.mixer.Sound(sound_path)
  sound.play()

def human():
  sound_path = random.choice(sounds_for_id[2])
  sound = pygame.mixer.Sound(sound_path)
  sound.play()

bufferTime = 1
gooseTimer = threading.Timer(bufferTime, goose)
catTimer = threading.Timer(bufferTime, cat)
humanTimer = threading.Timer(bufferTime, human)
timers = [gooseTimer, catTimer, humanTimer]

while True:

  ret, frame = cap.read()
  cv.imshow('Cam', frame)
  cv.imwrite(image_file_name, frame)

  results = tm_model.classify_frame(image_file_name)
  print("results:", results)

  current_id = results["id"]

  if previous_id != current_id and previous_id != None:
    timers[previous_id].cancel()

  if current_id in [0,1,2]:
    if not timers[current_id].is_alive():
      timers[current_id].start()
  previous_id = current_id

  k = cv.waitKey(1)
  if k % 256 == 27: break

cap.release()
cv.destroyAllWindows()