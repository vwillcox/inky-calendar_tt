import subprocess, shlex, os
import RPi.GPIO as GPIO
import signal

BUTTONS = [5, 6, 16, 24]

# These correspond to buttons A, B, C and D respectively
LABELS = ['A', 'B', 'C', 'D']

# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)

# Buttons connect to ground when pressed, so we should set them up
# with a "PULL UP", which weakly pulls the input signal to 3.3V.
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# "handle_button" will be called every time a button is pressed
# It receives one argument: the associated input pin.
def handle_button(pin):
    label = LABELS[BUTTONS.index(pin)]
    #print("Button press detected on pin: {} label: {}".format(pin, label))
    if pin == 5:
        subprocess.call(shlex.split('/usr/bin/python3 /home/pi/Inky-Impression-Weather-Station/once.py'))
    if pin == 16:
        subprocess.call(shlex.split('/usr/bin/python3 /home/pi/Pimoroni/inky/examples/clean.py --number 1'))
    if pin == 24:
        subprocess.call(shlex.split('/usr/bin/python3 /home/pi/inky-calendar/inky-calendar.py'))


# Loop through out buttons and attach the "handle_button" function to each
# We're watching the "FALLING" edge (transition from 3.3V to Ground) and
# picking a generous bouncetime of 250ms to smooth out button presses.
for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=250)

# Finally, since button handlers don't require a "while True" loop,
# we pause the script to prevent it exiting immediately.
signal.pause()
