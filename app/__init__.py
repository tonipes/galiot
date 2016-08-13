import RPi.GPIO as GPIO


import yaml
import falcon

from . import resource
from . import middleware
from . import sink
from .action.led_action import LedAction
from .action.servo_action import ServoAction

LED_PIN_RED = 25
LED_PIN_YELLOW = 24
LED_PIN_GREEN = 23

SERVO_PIN_BELL = 18

def get_config(filename):
    with open(filename, 'r') as f:
        return yaml.load(f)

config = get_config('config.yml')

# Global gpio stuff
GPIO.setmode(GPIO.BCM)

app = falcon.API(middleware=[
    middleware.AuthMiddleware(config['api_keys'])
])

actions = [
    ('led', LedAction(
        gpio=GPIO,
        led_pin_red=LED_PIN_RED,
        led_pin_yellow=LED_PIN_YELLOW,
        led_pin_green=LED_PIN_GREEN,
    )),
    ('servo', ServoAction(
        gpio=GPIO,
        servo_data_pin=SERVO_PIN_BELL,
        no_signal_sleep=True
    )),
]

action_res = resource.ActionResource(actions)
action_res_multi = resource.MultiActionResource(actions)

sink = sink.Sink()

app.add_sink(sink.get_sink, '/')

app.add_route('/action/', action_res_multi)
app.add_route('/action/{action_id}/', action_res)
