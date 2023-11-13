# Import core modules
import board
from digitalio import DigitalInOut, Direction

# Led class
class Led():

    # Initialisation
    def __init__(self, pin, invert, debug):
        print(f'Led.init({pin}, {invert}, {debug})')
        self.debug = debug
        # Initialise
        self.pin = pin
        self.dio = DigitalInOut(pin)
        self.dio.direction = Direction.OUTPUT
        self.invert = invert
        self.on = False
        # Turn off
        self.write(False)

    # Read function
    def read(self):
        if self.debug: print(f'Led.read({self.pin})={self.on}')
        return self.on

    # Write function
    def write(self, on):
        self.on = on
        if self.invert:
            on = not on
        self.dio.value = on
        if self.debug: print(f'Led.write({self.pin}, {self.on})')


# Led class (END)




