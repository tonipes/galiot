import time

from .gpio_action import GPIOAction

PWM_FREQ = 50

# Servo patterns: ( Target angle, Time before next step )
PATTENRS = {
    "ring_bell": [
        (0, 0.5),
        (90, 0.1),
        (-90, 0.3),
        (0, 0.5),
    ],
    "custom": [
        (60, 1),
        (-60, 1),
    ],
    "reset": [
        (-90, 1),
        (90, 1),
        (-45, 1),
        (45, 1),
        (0, 1),
        (-10, 0.1),
        (10, 0.1),
        (-5, 0.05),
        (5, 0.05),
        (-5, 0.02),
        (5, 0.02),
        (0, 0.5),
    ],
    "reset_slow": [
        (-90, 2),
        (90, 2),
        (0, 2),
        (-10, 0.1),
        (10, 0.1),
        (-5, 0.05),
        (5, 0.05),
        (-5, 0.02),
        (5, 0.02),
        (0, 0.5),
    ],
    "test": [
        (-90, 0.5),
        (90, 0.5),
        (-75, 0.4),
        (75, 0.4),
        (-50, 0.3),
        (50, 0.3),
        (-30, 0.2),
        (30, 0.2),
        (-20, 0.1),
        (20, 0.1),
        (-10, 0.05),
        (10, 0.05),
        (-5, 0.05),
        (5, 0.05),
    ],
}

# These are used only to calibrate hw, nothing else.
# Note that these should be checked if servo is changed.
# Even if the new servo is the same model as the old one.

DS_MAX = 12.1
DS_MID = 7.2
DS_MIN = 2.4

ANGLE_MAX = 90
ANGLE_MID = 0
ANGLE_MIN = -90

# Angular velocity in deg/sec. From servo's documentation.
# Used calculate sleep time after `pos` action
ANG_VEL = 600

class ServoAction(GPIOAction):
    def __init__(self, gpio, servo_data_pin, no_signal_sleep=False):
        """ If no_signal_sleep is set, servo will not get signal if pattern is not running
            This means that the servo won't try to keep its location when sleeping.
            Useful if there is some signal jittering and servo is making noise when sleeping """
        super(ServoAction, self).__init__(gpio)

        self.no_signal_sleep = no_signal_sleep
        self.servo_pin = servo_data_pin
        self.gpio.setup(self.servo_pin, self.gpio.OUT)
        self.pwm = self.gpio.PWM(self.servo_pin, PWM_FREQ)

        self.pwm.start(DS_MID)

        if self.no_signal_sleep:
            self.zero_signal()

    def zero_signal(self):
        # Sets servo off
        self.pwm.ChangeDutyCycle(0)

    def move_to_pos(self, pos):
        ds = self.pos_to_ds(pos)
        self.pwm.ChangeDutyCycle(ds)

    def max_move_time(self):
        return ANG_VEL / (ANGLE_MAX - ANGLE_MIN)

    # Simple linear mapper
    def pos_to_ds(self, pos):
        if pos > ANGLE_MAX:
            return ANGLE_MAX
        elif pos < ANGLE_MIN:
            return ANGLE_MIN
        elif pos > ANGLE_MID:
            ds = (pos - ANGLE_MID) * (DS_MAX - DS_MID) / (ANGLE_MAX - ANGLE_MID) + DS_MID
        else:
            ds = (pos - ANGLE_MIN) * (DS_MID - DS_MIN) / (ANGLE_MID - ANGLE_MIN) + DS_MIN
        return ds

    def run_action(self, action_id, params):
        if 'pos' in params.keys():
            pos = float(params['pos'])
            self.move_to_pos(pos)
            time.sleep(self.max_move_time())

        if 'pattern' in params.keys() and params['pattern'] in PATTENRS:
            pattern = PATTENRS[params['pattern']]
            times = params.get('times', 1)
            for times in range(times):
                for step in pattern:
                    self.move_to_pos(step[0])
                    time.sleep(step[1])

        if self.no_signal_sleep:
            self.zero_signal()