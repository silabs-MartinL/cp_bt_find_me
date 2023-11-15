# Import core modules
import board
import pwmio
import atexit

# Piezo class
class Piezo():

    # Initialisation
    def __init__(self, pin, debug):
        print(f'Piezo.init({pin}, {debug})')
        # Initialise
        self.debug = debug
        self.pin = pin
        self.pwmio = pwmio.PWMOut(pin, variable_frequency=True)
        atexit.register(self.deinit)
        self.on = False
        self.frequency = 0

    # Write function
    def write(self, frequency):
        # Valid frequency C0 to B8 ?
        if frequency >= 16 and frequency <= 7902: 
            self.on = True
            self.frequency = frequency
        else:
            self.on = False
            self.frequency = 0
        if self.on: 
            self.pwmio.frequency = self.frequency
            self.pwmio.duty_cycle = 0x8000
        else:
            self.pwmio.duty_cycle = 0
            self.pwmio.frequency = 262
        if self.debug: print(f'Piezo.write({self.pin}, {self.frequency})')

    # Deinit function
    def deinit(self):
        self.pwmio.duty_cycle = 0
        self.pwmio.deinit()
        atexit.deregister(self.deinit)
        if self.debug: print(f'Piezo.deinit({self.pin})')

# Piezo class (END)




