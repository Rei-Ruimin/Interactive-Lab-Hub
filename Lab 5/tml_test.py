import random
from teachable_machine_lite import TeachableMachineLite
import cv2 as cv
import pygame  # Import the pygame library
from collections import deque

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

# Stability check parameters
stability_threshold = 10  # Number of frames to consider the result stable
result_history = deque(maxlen=stability_threshold)

cap = cv.VideoCapture(0)

model_path = 'models/model.tflite'
image_file_name = "frame.jpg"
labels_path = "models/labels.txt"

tm_model = TeachableMachineLite(model_path=model_path, labels_file_path=labels_path)
previous_id = None

while True:

    ret, frame = cap.read()
    cv.imshow('Cam', frame)
    cv.imwrite(image_file_name, frame)
    
    results = tm_model.classify_frame(image_file_name)
    print("results:", results)
    
 
    current_id = results['id']
    result_history.append(current_id)
    
    # Check if the result is stable
    if (len(result_history) == stability_threshold and
        len(set(result_history)) == 1 and
        current_id in [0, 1, 2] and
        current_id != previous_id):
        sound_path = random.choice(sounds_for_id[current_id])
        sound = pygame.mixer.Sound(sound_path)
        sound.play()
        previous_id = current_id
    
    k = cv.waitKey(1)
    if k % 256 == 27:
        # press ESC to close camera view.
        break

cap.release()
cv.destroyAllWindows()
