from .gpio_action import GPIOAction

class LedAction(GPIOAction):
    def __init__(self, gpio, led_pin_red, led_pin_yellow, led_pin_green):
        super(LedAction, self).__init__(gpio)

        self.pins = {
            'red': led_pin_red,
            'yellow': led_pin_yellow,
            'green': led_pin_green,
        }

        self.states = {
            'red': False,
            'yellow': False,
            'green': False,
        }

        self.gpio.setup(self.pins['red'], self.gpio.OUT)
        self.gpio.setup(self.pins['yellow'], self.gpio.OUT)
        self.gpio.setup(self.pins['green'], self.gpio.OUT)

        self.gpio.output(self.pins['red'], self.gpio.LOW)
        self.gpio.output(self.pins['yellow'], self.gpio.LOW)
        self.gpio.output(self.pins['green'], self.gpio.LOW)

    def set_led(self, led_name, output):
        if output == self.gpio.HIGH:
            new_state = True
        else:
            new_state = False
        self.gpio.output(self.pins[led_name], output)
        self.states[led_name] = new_state

    def get_new_gpio_state(self, current_state, param):
        if param.lower() == "toggle" and current_state:
            return self.gpio.LOW
        elif param.lower() == "toggle":
            return self.gpio.HIGH
        else:
            return self.str2lvl(param)

    def set_pin(self, led_name, param_string):
        c_state = self.states[led_name]
        n_gpio_state = self.get_new_gpio_state(c_state, param_string)
        self.set_led(led_name, n_gpio_state)

    def run_action(self, action_id, params):
        if 'red' in params.keys():
            self.set_pin('red', params['red'])
        if 'yellow' in params.keys():
            self.set_pin('yellow', params['yellow'])
        if 'green' in params.keys():
            self.set_pin('green', params['green'])