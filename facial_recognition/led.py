# File to control the status of the LEDs
# there are three LEDs

from gpiozero import LED
import time


def led_op(op, pin, tm):
    print('Tried to switch on the LED pin no ::: ' + str(pin))
    led = LED(pin)
    if op == 'on':
        led.on()
    else:
        led.off()
