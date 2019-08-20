"""Maps acceleration (tilt) to Neopixel colors.

x, y, and z acceleration components map to red, green and blue,
respectively.

When the CPX is level, the lights are blue because there is no acceleration
on x or y, but on z, gravity pulls at 9.81 meters per second per second (m/s²).
When banking, the vertical (z) axis is no longer directly aligned with gravity,
so the blue decreases, and red increases because gravity is now pulling more
along the x axis. Similarly, when changing the pitch from level, we see blue change
to green.

This video walks you through the code: https://youtu.be/eNpPLbYx-iA
"""

import time
import board
import pulseio
from adafruit_circuitplayground.express import cpx


cpx.pixels.brightness = 0.2  # Adjust overall brightness as desired, between 0 and 1

print(dir(board))
print(dir(pulseio))






buzzer = pulseio.PWMOut(board.A0, variable_frequency=True)

#buzzer = pulseio.PWMOut(board.D2, variable_frequency=True)
# buzzer.frequency = 440
# OFF = 0
# ON = 2**15
# buzzer.duty_cycle = ON


def color_amount(accel_component):
    """Convert acceleration component (x, y, or z) to color amount (r, g, or b)"""
    standard_gravity = 9.81  # Acceleration (m/s²) due to gravity at the earth’s surface
    # Ignore the direction
    accel_magnitude = abs(accel_component)
    constrained_accel = min(
        accel_magnitude, standard_gravity)  # Constrain values
    normalized_accel = constrained_accel / standard_gravity     # Convert to 0–1
    # Convert to 0–255
    return round(normalized_accel * 255)


def format_acceleration(acceleration):
    return ', '.join(('{:>6.2f}'.format(axis_value) for axis_value in acceleration))


def format_rgb(rgb_amounts):
    return ', '.join(('{:>3d}'.format(rgb_amount) for rgb_amount in rgb_amounts))


def log_values(acceleration, rgb_amounts):
    print('({}) ==> ({})'.format(format_acceleration(
        acceleration), format_rgb(rgb_amounts)))


# while True:
#     acceleration = cpx.acceleration
#     rgb_amounts = [color_amount(axis_value) for axis_value in acceleration]
#     cpx.pixels.fill(rgb_amounts)
#     log_values()
#     time.sleep(0.1)


def sound_alarm():
    print('pound the alarm')
    cpx.play_file("police-siren-3.wav")
    # cpx.play_tone(500, 10)


def motion_happened(old, new):
    change = .5
    if old.x - new.x > change and old.y - new.y > change and old.z - new.z > change:
        return True
    return False


def get_acceleration():
    acceleration = cpx.acceleration
    rgb_amounts = [color_amount(axis_value) for axis_value in acceleration]
    cpx.pixels.fill(rgb_amounts)
    # log_values(acceleration, rgb_amounts)
    return acceleration


def run():
    acceleration = get_acceleration()
    while True:
        time.sleep(0.1)
        last_acceleration = acceleration
        acceleration = get_acceleration()
        if motion_happened(last_acceleration, acceleration):
            sound_alarm()
            run()


# audio = audioio.AudioOut(board.SPEAKER)
run()
