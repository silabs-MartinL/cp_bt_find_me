# Dev Lab: CircuitPython Bluetooth Find Me
![thumb](images/thumb.png)

## About

The video for this Dev Lab *will be* available on YouTube, where the video description includes links to further information.

This project based Dev Lab steps through the creation of a Find Me Bluetooth device, such as a key finder, using CircuitPython as the development language. 

The final device has the following features:

- Implements a Bluetooth device that conforms to the Bluetooth SIG Find Me profile
- Acts as a target device where an alert can be triggered remotely, including from a mobile phone
- Acts as a locator device where an alert can be triggered in a remote target device
- Audio alerts play RTTTL phone ringtones on a passive piezo buzzer using PWM output
- LEDs indicate the status of the device, including the alert state
- Buttons are used to control the operation of the device

## Usage

Two LEDs and two buttons are used to display status and control the device these are named mild and high to match the alert levels that can be set in the device. The passive piezo buzzer also plays RTTTL tunes when an alert state is set.

The LEDs and button assignments on each board are shown in the table below (see the Hardware section below for wiring information):

| Board / Name          | LED High       | LED Mild | Button High | Button Mild |
| --------------------- | -------------- | -------- | ----------- | ----------- |
| **xG24 Explorer Kit** | LED1           | LED0     | BTN1        | BTN0        |
| **xG24 Dev Kit**      | RED            | BLUE     | BTN1        | BTN0        |
| **SparkFun MGM240P**  | External (PB0) | STAT     | External () | External () |

### LED Indications

| Indication                                              | Meaning                                                      |
| ------------------------------------------------------- | ------------------------------------------------------------ |
| High and Mild flash on briefly together once per second | Device is advertising as a target, awaiting a connection     |
| High flashing rapidly                                   | Device is set to high alert level as a target, the piezo will play a tune in this state |
| Mild flashing rapidly                                   | Device is set to mild alert level as a target, the piezo will play a tune in this state |
| High on with a brief off period once per second         | Device is acting as a locator and will connect to any found targets to set them to high alert level |
| Mild on with a brief off period once per second         | Device is acting as a locator and will connect to any found targets to set them to mild alert level |

### Button Controls

Button functions are activated when the button is released.

A device in locator mode will continually scan for and set the alerts levels on any device in target mode. To fully cancel alerts it is necessary to first return the locator device to target mode, then cancel the alert locally on any sounding target device. 

This logic allows any target device in range to sound an alert on any device it come into range of even when moving around, thus maximising the chances of finding a lost device. It would be possible to alter the logic to reopen connections to any device it has alerted and cancel those alerts before returning to target mode, however for reliable operation the target devices will need to still be in range of the locator.

| State                                            | Button Controls                                              |
| ------------------------------------------------ | ------------------------------------------------------------ |
| Device is in target mode, alert level is set     | Any: Cancels alert on local device (will be turned back on if a device is running in locator mode nearby) |
| Device is in target mode, alert level is not set | High: swaps to locator mode setting high alert on any found targets |
|                                                  | Mild: swaps to locator mode setting mild alert on any found targets |
| Device is in locator mode                        | Any: Cancels locator mode and returns to target mode         |



## Files and Folders

**device_root_target:** Contains the software for step 1 which acts as a target device only. 

**device_root_target_locator:** Contains the software for step 2 which adds the ability to act as a locator device in addition to a target device. 

To program your device copy the files and folders, from one of the folders above, into the root of your CircuitPython device.

## Hardware

The software will run on three different development boards featuring the EFR32MG24 wireless microcontroller. The software will run without a piezo buzzer by indicating alert status on the LEDs, but adding a passive piezo buzzer will allow the audio alerts to be heard. 

The assignment of pins to functions can be found at the start of App.py and can be altered as necessary. The default assignments for external components are described in the sections below.

### Silicon Labs xG24 Explorer Kit

This is simplest board to work with as the passive piezo buzzer can be easily connected to the mikro BUS connector if you add pins to the passive piezo buzzer wires. The LEDs and buttons are already present on this board. 

The table and image below show the required connections:

| **xg24 Explorer Kit** | External Components           |
| --------------------- | ----------------------------- |
| mikro BUS: GND        | Passive Piezo: Ground (black) |
| mikro BUS: PWM (PA0)  | Passive Piezo: Signal (red)   |

**![piezo-exp](images/piezo-exp.png)**

### **Silicon Labs xG24 Dev Kit**

**This board also has the required buttons and LEDs on board, but the passive piezo buzzer needs to be connected to the expansion header slots at the side of the board. You may find it easier to fit header sockets to the Dev Kit and pins to the passive piezo buzzer.** 

**This board also has a slot for a coin cell and a connector for an external battery for portable use.** 

**The table and image below show the required connections:**

| **xg24 Dev Kit**            | **External Components**           |
| --------------------------- | --------------------------------- |
| **Expansion: pin 1 (GND)**  | **Passive Piezo: Ground (black)** |
| **Expansion: pin 10 (PA7)** | **Passive Piezo: Signal (red)**   |

**![piezo-dev](images/piezo-dev.png)**

### SparkFun Thing Plus MGM240P

The software will also run on this board but you will need to add an LED and two buttons in addition to the piezo buzzer. 

This board has a connector for an external battery for portable use.

The table below shows the required connections and the wiring diagram shows breadboard wiring with rows of header pins for the SparkFun board:

| xg24 Dev Kit | External Components                 |
| ------------ | ----------------------------------- |
| GND          | Passive Piezo: Ground (black)       |
| C7           | Passive Piezo: Signal (red)         |
| B0           | LED+ (with 2.2k pull-down resistor) |
| A4           | Button+ (with 1k pull-up resistor)  |
| B2           | Button+ (with 1k pull-up resistor)  |

**![SparkFun-MGM240P-Expansion_bb](images/expanded-sparkfun.png)**

