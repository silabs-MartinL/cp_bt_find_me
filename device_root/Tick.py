# Import core modules
import supervisor

# Constants
_TICKS_PERIOD = const(1<<29)
_TICKS_MAX = const(_TICKS_PERIOD-1)
_TICKS_HALFPERIOD = const(_TICKS_PERIOD//2)
_TICKS_DURATION_MAX = const(_TICKS_HALFPERIOD-1)

# Tick class
class Tick():

    # Initialisation
    def __init__(self, name, duration, repeat, debug):
        print(f'Tick.init({name}, {duration}, {repeat}, {debug})')
        # Initialise
        self.debug = debug
        self.name = name
        self.write(duration, repeat)

    # Read function
    def read(self):
        fired = False
        if self.on:
            now = supervisor.ticks_ms()
            diff = (now - self.start) & _TICKS_MAX
            diff = ((diff + _TICKS_HALFPERIOD) & _TICKS_MAX) - _TICKS_HALFPERIOD
            if diff >= self.duration:
                fired = True
                if self.repeat:
                    self.write(self.duration, self.repeat)
                else:
                    self.write(0, False)
        if self.debug and fired: print(f'Tick.read({self.name}) = {self.on}, {fired}')
        return self.on, fired

    # Write function
    def write(self, duration, repeat):
        self.duration = duration
        self.repeat = repeat
        if self.duration > _TICKS_DURATION_MAX:
            self.duration = _TICKS_DURATION_MAX
        if self.duration > 0:
            self.on = True
        else:
            self.on = False
        self.start = supervisor.ticks_ms()
        if self.debug: print(f'Tick.write({self.name}, {self.duration}, {self.repeat})={self.on}')            
        return self.on

# Tick class (END)




