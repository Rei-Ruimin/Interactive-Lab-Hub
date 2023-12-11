import RPi.GPIO as GPIO
from time import sleep

import digitalio, board

pin_motor = board.D26

def initMotor():

  pin_gpio = digitalio.DigitalInOut(pin_motor)
  pin_gpio.direction = digitalio.Direction.OUTPUT
  pin_gpio.value = False
  return pin_gpio

def runMotor(pin_gpio):

  pin_gpio.value = True
  sleep(1)
  pin_gpio.value = False