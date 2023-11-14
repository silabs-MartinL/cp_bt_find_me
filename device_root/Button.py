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
        self.state = 0b0

    # Main function, call to update state
    # Returns: 
    #   0 = off, unchanged
    #   1 = on,  unchanged
    #   2 = off, changed
    #   3 = on,  changed
    def main(self):
        self.state = 0b0
        on = self.dio.value
        if self.invert:
            on = not on
        if self.on != on:
            self.state |= 0b10
            if on:
                self.state |= 0b1
            self.on = on
        if self.debug and changed: print(f'Button.read({self.pin}) = {self.state}')
        return self.state

    # State function, returns last read button state, without a new read
    # Returns: 
    #   0 = off, unchanged
    #   1 = on,  unchanged
    #   2 = off, changed
    #   3 = on,  changed
    def state(self):
        return self.state        

# Button class (END)




