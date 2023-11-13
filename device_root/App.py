# Import core modules
import board

# Import library modules
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import Advertisement
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement

# Import application modules
from Button import Button
from Led import Led
from Piezo import Piezo
from Tick import Tick
from ImmediateAlertService import ImmediateAlertService

# Application class
class App():

    # Initialisation
    def __init__(self, debug):
        self.debug = True
        if self.debug: print(f'App.init()')
        # Hardware (board IDs: explorerkit_xg24_brd2703a, devkit_xg24_brd2601b, sparkfun_thingplus_matter_mgm240p_brd2704a)
        self.hw = {}
        if board.board_id == "explorerkit_xg24_brd2703a":
            self.hw["init"]  = True
            self.hw["btn0"]  = Button(board.PB2, True, False)
            self.hw["btn1"]  = Button(board.PB3, True, False)
            self.hw["led0"]  = Led(board.PA4, False, False)
            self.hw["led1"]  = Led(board.PA7, False, False)  
            self.hw["piezo"] = Piezo(board.PA0, False) # MIKROE_PWM  
        else:
            self.hw["init"] = False
            print(f'App.init() ERROR: Unsupported board: {board.board_id}')
        # Tick timers
        self.ticks = {}
        self.ticks["leds"] = Tick("leds", 100, True, False)
        self.ticks["piezo"] = Tick("piezo", 250, True, False)
        # Data
        self.data = {}
        self.data["leds_bit"] = 0b1
        self.data["leds_mask"] = 0b1111111111
        self.data["led0_mask"] = 0b0
        self.data["led1_mask"] = 0b0
        self.data["piezo_scale"] = [261, 294, 330, 349, 392, 440, 494, 523]
        self.data["piezo_index"] = None
        # Bluetooth
        self.ble = {}
        self.ble["locate"] = False
        self.ble["connected"] = False
        self.ble["alert_level"] = 0
        self.ble["radio"] = BLERadio()
        self.ble["ias"] = ImmediateAlertService()
        self.ble["ad"] = ProvideServicesAdvertisement(self.ble["ias"])
        self.ble["ad"].short_name = "Silabs Find Me"
        self.ble["ad"].connectable = True

    # Main function (called repeatedly do not block)
    def main(self):
        #if self.debug: print(f'App.main() ENTER t={time.monotonic()} m={self.data["main"]}')

        # Buttons off and unchanged
        btn0_on = btn0_change = False
        btn1_on = btn1_change = False
        # Read buttons
        if "btn0" in self.hw: btn0_on, btn0_change = self.hw["btn0"].read()
        if "btn1" in self.hw: btn1_on, btn1_change = self.hw["btn1"].read()

        # Running as target (not locator) ?
        if not self.ble["locate"]:

            # Not connected ?
            if not self.ble["radio"].connected:
                # Not advertising ?
                if not self.ble["radio"].advertising:
                    # Begin advertising
                    self.ble["radio"].start_advertising(self.ble["ad"])
                    if self.debug: print(f'start_advertising()')
            # Connected ?
            else:
                # Advertising ?
                if self.ble["radio"].advertising:
                    # Stop advertising
                    self.ble["radio"].stop_advertising()
                    if self.debug: print(f'stop_advertising()')
       
            # Alert level is set ?
            if self.ble["ias"].alert_level != 0:
                # Has any button been pressed ?
                if (btn0_change and btn0_on) or (btn1_change and btn1_on):
                    # Cancel alert
                    self.ble["ias"].alert_level = 0
              
            # Connected - double flash LED0
            if self.ble["radio"].connected: self.data["led0_mask"] = 0b101
            # Advertising - single flash LED0
            elif self.ble["radio"].advertising: self.data["led0_mask"] = 0b1
            # Else - turn off LED0
            else: self.data["led0_mask"] = 0b0
            # High alert - double flash LED1
            if self.ble["ias"].alert_level > 1: self.data["led1_mask"] = 0b101
            # Mid alert - single flash LED1
            elif self.ble["ias"].alert_level == 1: self.data["led1_mask"] = 0b1
            # Else - turn off LED1
            else: self.data["led1_mask"] = 0b0  
    
        # Connected changed ?
        if self.ble["connected"] != self.ble["radio"].connected:
            self.ble["connected"] = self.ble["radio"].connected
            if self.debug:
                if self.ble["connected"]: print(f'Connected')
                else: print(f'Disconnected')
        # Alert level changed ?
        if self.ble["alert_level"] != self.ble["ias"].alert_level:
            self.ble["alert_level"] = self.ble["ias"].alert_level
            if self.debug:
                if self.ble["alert_level"] > 1: print(f'Alert level high')
                elif self.ble["alert_level"] == 1: print(f'Alert level mild')
                else: print(f'Alert level none')

        # Read piezo tick timer
        tick_piezo_on, tick_piezo_fired = self.ticks["piezo"].read()
        # Piezo tick timer fired ?
        if tick_piezo_fired:
            # High alert level ?
            if self.ble["ias"].alert_level > 1:
                # Validate index
                if self.data["piezo_index"] == None or self.data["piezo_index"] < 0 or self.data["piezo_index"] >= len(self.data["piezo_scale"]):
                    # Start at beginning of scale
                    self.data["piezo_index"] = 0
                # Play note
                self.hw["piezo"].write(True, self.data["piezo_scale"][self.data["piezo_index"]])
                # Rising scale
                self.data["piezo_index"] += 1
            # Mild alert level ?
            elif self.ble["ias"].alert_level == 1:
                # Validate index
                if self.data["piezo_index"] == None or self.data["piezo_index"] < 0 or self.data["piezo_index"] >= len(self.data["piezo_scale"]):
                    # Start at end of scale
                    self.data["piezo_index"] = len(self.data["piezo_scale"])-1
                # Play note
                self.hw["piezo"].write(True, self.data["piezo_scale"][self.data["piezo_index"]])
                # Falling scale
                self.data["piezo_index"] -= 1
            # No alert level ?
            else:
                # Piezo is sounding ?
                if self.data["piezo_index"] != None:
                    # Turn off
                    self.data["piezo_index"] = None
                    # Stop playing note
                    self.hw["piezo"].write(False, self.data["piezo_scale"][0])

        # Read leds tick timer
        tick_leds_on, tick_leds_fired = self.ticks["leds"].read()
        # Led tick timer fired ?
        if tick_leds_fired:
            # Safety check leds bit
            if self.data["leds_bit"] & self.data["leds_mask"] == 0b0:
                self.data["leds_bit"] = 0b1 
            # LED0 initialised ?
            if "led0" in self.hw:
                # Update led0
                if self.data["leds_bit"] & self.data["led0_mask"]:
                    self.hw["led0"].write(True)
                else:
                    self.hw["led0"].write(False)
            # LED1 initialised ?
            if "led1" in self.hw:
                # Update led0
                if self.data["leds_bit"] & self.data["led1_mask"]:
                    self.hw["led1"].write(True)
                else:
                    self.hw["led1"].write(False)                    
            # Update leds bit
            self.data["leds_bit"] <<= 1

        # Return buttons
        return True

# Application class (END)



