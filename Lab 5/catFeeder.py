import random
import cv2 as cv
import pygame
from collections import deque

from image import displayImage
from init import init, getSoundsDict, getAnimalsDict
from motor import runMotor

import threading

def playSound(sound):

    soundPath = random.choice(sound)
    sound = pygame.mixer.Sound(soundPath)
    sound.play()

def main():

    # Initialize Everything
    disp, rotation, model, pinMotor = init()
    cap = cv.VideoCapture(0)

    # Setup Stability Parameters
    threshold = 10
    history = deque(maxlen=threshold)
    for i in range(10): history.append(i)

    # Other Variables
    imagePath = "frame.jpg"
    prevID = None

    # Get Dictionaries
    sounds = getSoundsDict()
    animals = getAnimalsDict()

    while True:

        ret, frame = cap.read()
        cv.imshow('Cam', frame)
        cv.imwrite(imagePath, frame)

        results = model.classify_frame(imagePath)
        print("Results:", results)

        history.append(currID:=results["id"])

        if all([len(set(history)) == 1, currID in [0,1,2], currID != prevID]):

            playSound(sounds[currID])
            prevID = currID

            if currID == 1:
                thread = threading.Thread(target=runMotor, args=[pinMotor])
                thread.start()

            displayImage(animals[currID], disp, rotation)

        elif all([len(set(history)) == 1, currID != prevID]):

            displayImage(animals[3], disp, rotation)

        if cv.waitKey(1) % 256 == 27: break

    cap.release
    cv.destroyAllWindows()

if __name__ == "__main__":
    main()