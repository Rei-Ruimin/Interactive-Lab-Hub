from motor import runMotor, initMotor
import RPi.GPIO as GPIO
from time import sleep

import digitalio
import board

pin = digitalio.DigitalInOut(board.D26)
pin.direction = digitalio.Direction.OUTPUT
pin.value = True
sleep(1)
pin.value = False
sleep(1)