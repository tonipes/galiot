import RPi.GPIO as GPIO

from .action import Action

class GPIOAction(Action):
    def __init__(self, gpio):
        self.gpio = gpio
        
    def str2lvl(self, level_string):
        level_string = level_string.lower()
        if level_string == 'high':
            return GPIO.HIGH
        else:
            return GPIO.LOW