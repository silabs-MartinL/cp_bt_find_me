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
from Rtttl import Rtttl
from Tick import Tick
from ImmediateAlertService import ImmediateAlertService

# Application class
class App():

    # Initialisation
    def __init__(self, debug):
        self.debug = True
        if self.debug: print(f'App.init()')
        # Initialised
        self.on = False
        # Hardware (board IDs: explorerkit_xg24_brd2703a, devkit_xg24_brd2601b, sparkfun_thingplus_matter_mgm240p_brd2704a)
        self.hw = {}
        if board.board_id == "explorerkit_xg24_brd2703a":
            self.on              = True
            self.hw["btn_high"]  = Button(board.PB3, True, False) # BTN1
            self.hw["btn_mild"]  = Button(board.PB2, True, False) # BTN0
            self.hw["led_ble"]   = Led(board.PA4, False, False) # LED0
            self.hw["led_alert"] = Led(board.PA7, False, False) # LED1 
            self.hw["rtttl"]     = Rtttl(board.PA0, True) # MIKROE_PWM
        elif board.board_id == "devkit_xg24_brd2601b":
            self.on              = True
            self.hw["btn_high"]  = Button(board.PB3, True, False) # BTN1
            self.hw["btn_mild"]  = Button(board.PB2, True, False) # BTN0
            self.hw["led_ble"]   = Led(board.PB0, False, False) # BLUE
            self.hw["led_alert"] = Led(board.PD2, False, False) # RED (PA4=GREEN)  
            self.hw["rtttl"]     = Rtttl(board.PA7, True) # SPI_CS (header 10 - may clash with IMU) 
        elif board.board_id == "sparkfun_thingplus_matter_mgm240p_brd2704a":
            self.on              = True
            self.hw["btn_high"]  = Button(board.PB2, True, False) # (external)
            self.hw["btn_mild"]  = Button(board.PA4, True, False) # (external)
            self.hw["led_ble"]   = Led(board.PA8, False, False) # BLUE (on board)
            self.hw["led_alert"] = Led(board.PB0, False, False) # (external)   
            self.hw["rtttl"]     = Rtttl(board.PB1, True)
        else:
            print(f'App.init() ERROR: Unsupported board: {board.board_id}')
        # App is on ?
        if self.on:
            # Tick timers
            self.ticks = {}
            self.ticks["leds"] = Tick("leds", 100, True, False)
            # Data
            self.data = {}
            self.data["leds_bit"] = 0b1
            self.data["leds_mask"] = 0b1111111111
            self.data["led_ble_mask"] = 0b0
            self.data["led_alert_mask"] = 0b0
            self.data["tune_name_high"] = self.hw["rtttl"].load("knightrh:d=4,o=6,b=90:16d.5,32d#.5,32d.5,8a.5,16d.,32d#.,32d.,8a.5,16d.5,32d#.5,32d.5,16a.5,16d.,2c,16d.5,32d#.5,32d.5,8a.5,16d.,32d#.,32d.,8a.5,16d.5,32d#.5,32d.5,16a.5,16d.,2d#,a4,32a#.4,32a.4,d5,32d#.5,32d.5,2a5,16c.,16d.", False)
            self.data["tune_name_mild"] = self.hw["rtttl"].load("knightrl:d=4,o=5,b=125:16e,16p,16f,16e,16e,16p,16e,16e,16f,16e,16e,16e,16d#,16e,16e,16e,16e,16p,16f,16e,16e,16p,16f,16e,16f,16e,16e,16e,16d#,16e,16e,16e,16d,16p,16e,16d,16d,16p,16e,16d,16e,16d,16d,16d,16c,16d,16d,16d,16d,16p,16e,16d,16d,16p,16e,16d,16e,16d,16d,16d,16c,16d,16d,16d", False)
            # Bluetooth
            self.ble = {}
            self.ble["locate_state"] = 0
            self.ble["locate_level"] = 0
            self.ble["connected"] = False
            self.ble["connection"] = None
            self.ble["alert_level"] = 0
            self.ble["radio"] = BLERadio()
            self.ble["ias"] = ImmediateAlertService()
            self.ble["ad"] = ProvideServicesAdvertisement(self.ble["ias"])
            self.ble["ad"].short_name = "Find Me"
            self.ble["ad"].connectable = True

    # Main function (called repeatedly do not block)
    def main(self):
        #if self.debug: print(f'App.main() ENTER t={time.monotonic()} m={self.data["main"]}')
        # App is on ? 
        if self.on:
            # Read buttons
            self.hw["btn_high"].read()
            self.hw["btn_mild"].read()
            # Read tick timers
            self.ticks["leds"].read()
 
            # Running as target (not locator) ?
            if self.ble["locate_state"] == 0:

                # Has any button been released ?
                if self.hw["btn_high"].released or self.hw["btn_mild"].released:
                    # Alert level is set ?
                    if self.ble["ias"].alert_level == 1 or self.ble["ias"].alert_level == 2:
                        # Cancel alert
                        self.ble["ias"].alert_level = 0
                    # Alert level is not set ?
                    else:
                        # Not connected ?
                        if not self.ble["radio"].connected:
                            # Run as locator
                            self.ble["locate_state"] = 1
                            print(f'Locator')
                            # High button released ?
                            if self.hw["btn_high"].released: 
                                # Set high alert
                                self.ble["locate_level"] = 2
                            # Mild button released ?
                            elif self.hw["btn_mild"].released: 
                                # Set mild alert
                                self.ble["locate_level"] = 1
                            # Advertising ?
                            if self.ble["radio"].advertising:
                                # Stop advertising
                                self.ble["radio"].stop_advertising()
                                if self.debug: print(f'stop_advertising()')                                

                # Still running as target (not locator) ?
                if self.ble["locate_state"] == 0:
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
        
                    # Connected - double flash LED0
                    if self.ble["radio"].connected: self.data["led_ble_mask"] = 0b101
                    # Advertising - single flash LED0
                    elif self.ble["radio"].advertising: self.data["led_ble_mask"] = 0b1
                    # Else - turn off LED0
                    else: self.data["led_ble_mask"] = 0b0

                    # High alert - double flash LED1
                    if self.ble["ias"].alert_level > 1: self.data["led_alert_mask"] = 0b101
                    # Mid alert - single flash LED1
                    elif self.ble["ias"].alert_level == 1: self.data["led_alert_mask"] = 0b1
                    # Else - turn off LED1
                    else: self.data["led_alert_mask"] = 0b0    

            # Running as locator (not target) ?    
            else:
                # Has any button been released ?
                if self.hw["btn_high"].released or self.hw["btn_mild"].released:
                    # Run as target CANCEL ALARMS, DISCONNECT
                    self.ble["locate_state"] = 0
                    print(f'Target')
                    pass

                # Still running as locator ? 
                if self.ble["locate_state"] != 0:
                    # Update alert led
                    if self.ble["locate_level"] == 2:
                        # Double deflash on LED1
                        self.data["led_alert_mask"] = 0b1111111010
                    elif self.ble["locate_level"] == 1:
                        # Single deflash on LED1
                        self.data["led_alert_mask"] = 0b1111111110  
                    else:
                        # LED 1 is on
                        self.data["led_alert_mask"] = 0b1111111111

                    # Scanning ? 
                    if self.ble["locate_state"] == 1:
                        # Start scan, loop through ads
                        if self.debug: print(f'start_scan()')
                        target_ads = {}
                        for ad in self.ble["radio"].start_scan(ProvideServicesAdvertisement, timeout=0.1):
                            # Immediate alert service in advertisement ?
                            if self.ble["ias"] in ad.services:
                                # Save ad
                                target_ads[ad.address] = {}
                                target_ads[ad.address]["short_name"] = ad.short_name
                        if self.debug: print(f'{target_ads}')
                        # Single deflash
                        self.data["led_ble_mask"] = 0b1111111110                    

            # Common code
            # Connected changed ?
            if self.ble["connected"] != self.ble["radio"].connected:
                self.ble["connected"] = self.ble["radio"].connected
                if self.debug:
                    if self.ble["connected"]: print(f'Connected')
                    else: print(f'Disconnected')

            # Alert level changed ?
            if self.ble["alert_level"] != self.ble["ias"].alert_level:
                self.ble["alert_level"] = self.ble["ias"].alert_level
                if self.ble["alert_level"] > 1:
                    if self.debug: print(f'Alert level high')
                    if self.hw["rtttl"].play_name != self.data["tune_name_high"]:
                        self.hw["rtttl"].play(self.data["tune_name_high"], True)
                elif self.ble["alert_level"] == 1:
                    if self.debug: print(f'Alert level mild')
                    if self.hw["rtttl"].play_name != self.data["tune_name_mild"]:
                        self.hw["rtttl"].play(self.data["tune_name_mild"], True)   
                else:
                    if self.debug: print(f'Alert level none')
                    if self.hw["rtttl"].play_name != None:
                        self.hw["rtttl"].stop()  
            # Drive rtttl
            self.hw["rtttl"].main()                                                

            # Led tick timer fired ?
            if self.ticks["leds"].fired:
                # Safety check leds bit
                if self.data["leds_bit"] & self.data["leds_mask"] == 0b0:
                    self.data["leds_bit"] = 0b1 
                # LED0 initialised ?
                if "led_ble" in self.hw:
                    # Update led0
                    if self.data["leds_bit"] & self.data["led_ble_mask"]:
                        self.hw["led_ble"].write(True)
                    else:
                        self.hw["led_ble"].write(False)
                # LED1 initialised ?
                if "led_alert" in self.hw:
                    # Update led0
                    if self.data["leds_bit"] & self.data["led_alert_mask"]:
                        self.hw["led_alert"].write(True)
                    else:
                        self.hw["led_alert"].write(False)                    
                # Update leds bit
                self.data["leds_bit"] <<= 1

# Application class (END)




