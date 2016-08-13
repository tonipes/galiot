# Galiot
> Small IoT thing

## API

### Method one: Request body

Use request body to trigger multiple actions:

```
URL: http://www.device.com/action/

Body:
{
  "actions":[
    {
      "action_id": "servo",
      "params": {
        "pattern": "ring_bell",
        "times": 5
      }
    },
    {
      "action_id": "led",
      "params": {
        "red": "high",
        "green": "low",
        "yellow": "toggle"
      }
    }
  ]
}
```

### Method two: Query strings

Only one action can be triggered with single request

```
http://www.med_device.com/action/led?red=high&yellow=toggle
or
http://www.med_device.com/action/servo?pos=0&pattern=reset&times=2
```

# Action types
  - **servo**
    - For controlling the servo
    - Parameters:
      - **pattern**: Name of the pattern to run
      - **times**: How many times pattern in run
      - **pos**: Set servo to angle. This is run before patterns
        - Use angle values between -90 and 90
      - Note that if there are multiple servo actions running on the same time, result may not be pretty.
  - **led**
    - For controlling the on-board traffic light LEDs
    - Parameters:
      - **red**: To set red LED
      - **yellow**: To set yellow LED
      - **green**: To set green LED
    - Possible values are: `high, low, toggle`

# Request relay (not yet implemented)

If you want to use slave devices with the main device, you can use the `relay_action` to forward actions to different devices eg. `ESP8266` wifi microcontroller.

Register slave device to the main Maitolabra Electromechanical Device:

```
http://www.med_device.com/register/&action=led
```

This would register the device sending this request to be interested in all `led` actions.

When the Maitolabra Electromechanical Device gets a `led` action trigger request, it will relay the action to all devices that are registered to be interested `led` action triggers.

