from PIL import Image
from time import sleep

def scaleImage(path, disp):

    image = Image.open(path).convert("RGBA")

    image_ratio = image.width / image.height
    screen_ratio = disp.height / disp.width

    if screen_ratio < image_ratio:
        scaled_width = image.width * disp.width // image.height
        scaled_height = disp.width
    else:
        scaled_width = disp.height
        scaled_height = image.height * disp.height // image.width

    x = scaled_width // 2 - disp.height // 2
    y = scaled_height // 2 - disp.width // 2
    image = image.crop((x, y, x + disp.height, y + disp.width))

    return image

def displayImage(animal, disp, rotation):

    if animal != "BLANK": path = f"./images/{animal}1.png"
    else: path = f"./images/BLANK.png"

    scaled_image = scaleImage(path, disp)
    disp.image(scaled_image, rotation)

    if animal == "BLANK": return
    sleep(1)

    path = f"./images/{animal}2.png"
    scaled_image = scaleImage(path, disp)
    disp.image(scaled_image, rotation)
