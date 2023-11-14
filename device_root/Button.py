# Import core modules
import board
from digitalio import DigitalInOut, Direction

# Button class
class Button():

    # Initialisation
    def __init__(self, pin, invert, debug):
        print(f'Button.init({pin}, {invert}, {debug})')
        # Initialise
        self.debug = debug        
        self.pin = pin
        self.dio = DigitalInOut(pin)
        self.dio.direction = Direction.INPUT
        self.invert = invert
        self.on = False
        self.changed = False
        self.pressed = False
        self.released = False

    # Read function, call to update state
    def read(self):
        self.changed = False
        self.pressed = False
        self.released = False
        on = self.dio.value
        if self.invert:
            on = not on
        if self.on != on:
            self.on = on
            self.changed = True
            self.pressed = self.on
            self.released = not self.on
        if self.debug and self.changed: print(f'Button.read({self.pin}) = {self.changed} [r={self.released}, p={self.pressed}, o={self.on}]')
        return self.changed

# Button class (END)




