import adafruit_rgb_display.st7789 as st7789
import digitalio, board
import pygame

from PIL import Image, ImageDraw, ImageFont
from teachable_machine_lite import TeachableMachineLite
from motor import initMotor

def initDisp():

  return st7789.ST7789(
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

def initDisplay(disp, rotation):

  image = Image.new("RGB", (disp.height, disp.width))

  draw = ImageDraw.Draw(image)
  draw.rectangle((0, 0, disp.height, disp.width), outline=0, fill=(0, 0, 0))
  disp.image(image, rotation)

  backlight = digitalio.DigitalInOut(board.D22)
  backlight.switch_to_output()
  backlight.value = True

def getFont():

  return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)

def getSoundsDict():

  return {
    0: ['sound_effects/goose/1.mp3'],
    1: ['sound_effects/cat/1.mp3', 'sound_effects/cat/2.mp3', 'sound_effects/cat/3.mp3'],
    2: ['sound_effects/human/1.mp3']
  }

def getAnimalsDict():

  return {
    0: "GOOSE",
    1: "CAT",
    2: "HUMAN",
    3: "BLANK"
  }

def getFilesDict():

  return {
    0: "./images/GOOSE1.png",
    1: "./images/CAT1.png",
    2: "./images/BLANK.png",
    3: "./images/BLANK.png"
  }

def init():

  # Display
  disp = initDisp()
  rotation = 90

  initDisplay(disp, rotation)

  # Pygame
  pygame.mixer.init()
  # cap = cv.VideoCapture(0)

  # Model
  model = TeachableMachineLite(
    model_path="models/model.tflite",
    labels_file_path="models/labels.txt"
  )
  # Motor
  pinMotor = initMotor()

  return disp, rotation, model, pinMotor