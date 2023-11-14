# Import core modules
import board

# Import application modules
from Piezo import Piezo
from Tick import Tick

# Rtttl class
# Lots of examples at: https://huggingface.co/datasets/cosimoiaia/RTTTL-Ringtones/tree/main
class Rtttl():

    # Initialisation
    def __init__(self, piezo, debug):
        print(f'Rtttl.init({debug})')
        # Initialise
        self.debug = debug
        self.piezo = piezo
        # Frequencies
        self.frequencies = {}
        self.frequencies["p"]   = 0
        self.frequencies["c4"]  = 262
        self.frequencies["c#4"] = 277
        self.frequencies["d4"]  = 294
        self.frequencies["d#4"] = 311
        self.frequencies["e4"]  = 330
        self.frequencies["f4"]  = 349
        self.frequencies["f#4"] = 370
        self.frequencies["g4"]  = 392
        self.frequencies["g#4"] = 415  
        self.frequencies["a4"]  = 440
        self.frequencies["a#4"] = 466
        self.frequencies["b4"]  = 494
        self.frequencies["c5"]  = 523
        self.frequencies["c#5"] = 554
        self.frequencies["d5"]  = 587
        self.frequencies["d#5"] = 622
        self.frequencies["e5"]  = 659
        self.frequencies["f5"]  = 698
        self.frequencies["f#5"] = 740
        self.frequencies["g5"]  = 784 
        self.frequencies["g#5"] = 831
        self.frequencies["a5"]  = 880
        self.frequencies["a#5"] = 932
        self.frequencies["b5"]  = 988
        self.frequencies["c6"]  = 1047
        self.frequencies["c#6"] = 1109
        self.frequencies["d6"]  = 1175
        self.frequencies["d#6"] = 1245
        self.frequencies["e6"]  = 1319
        self.frequencies["f6"]  = 1397
        self.frequencies["f#6"] = 1480
        self.frequencies["g6"]  = 1568
        self.frequencies["g#6"] = 1661 
        self.frequencies["a6"]  = 1760
        self.frequencies["a#6"] = 1865
        self.frequencies["b6"]  = 1976
        self.frequencies["c7"]  = 2093
        self.frequencies["c#7"] = 2217
        self.frequencies["d7"]  = 2349
        self.frequencies["d#7"] = 2489
        self.frequencies["e7"]  = 2637
        self.frequencies["f7"]  = 2794
        self.frequencies["f#7"] = 2960
        self.frequencies["g7"]  = 3136
        self.frequencies["g#7"] = 3322 
        self.frequencies["a7"]  = 3520
        self.frequencies["a#7"] = 3729
        self.frequencies["b7"]  = 3951
        # Load a tune
        self.notes = []
        #self.load("friends1:d=8,o=5,b=180:b,16b,16a,16g,f,f,16g,a,4g,b,16b,16a,16g,f,f,16g,a,4g,4,6d,g,a,c6,b,a,g.,16g,d,g,a,2a,16d,g,a,c6,b,a,g.,16c6,b,a,g,2d6,16c6,c6,c6,c6,b,a,g.,16a,b,4b,16g,16a,16b,16c6,c6,c6,c6,c6,b,a,g,g.,16d,16g,16a,b,4a,4g,d,6,c6,4b,16a,g,b.,a")
        self.load("missioni:d=4,o=5,b=112:8d#.,8d#.,8d#.,8d#.,8f#,16g#,16f#,8d#.,8d#.,8d#.,8d#,16d#,8c#,8d,8d#.,8d#.,8d#.,8d#.,8f#,16g#,16f#,8d#.,8d#.,8d#.,8d#,16d#,8c#,8d,8d#,16p,8d#,16p,8d#,16p,8d#,16p,16f#,16p,16g#,16p,8d#,16p,8d#,16p,8d#,16p,8d#,16p,16c#,16p,16d,16p,16d#,16p,16c#,16d#,16p,16c#,16d#,16p,16c#,16d#,16p,16f#,16p,16g#,16f#,16d#,16p,16c#,16d#,16p,16c#,16d#,16p,16c#,16d#,16p,8c#,8d,16a#,16g,2d#,32p,16a#,16g,2d,32p,16a#,16g,2c#,16p,16a#,16c")
        #self.load("dualingbanjos:d=4,o=5,b=200:8c#,8d,e,c#,d,b4,c#,d#4,b4,p,16c#6,16p,16d6,16p,8e6,8p,8c#6,8p,8d6,8p,8b,8p,8c#6,8p,8a,8p,b,p,a4,a4,b4,c#,d#4,c#,b4,p,8a,8p,8a,8p,8b,8p,8c#6,8p,8a,8p,8c#6,8p,8b")
        #self.load("flinston:d=4,o=5,b=40:32p,16f6,16a#,16a#6,32g6,16f6,16a#.,16f6,32d#6,32d6,32d6,32d#6,32f6,16a#,16c6,d6,16f6,16a#.,16a#6,32g6,16f6,16a#.,32f6,32f6,32d#6,32d6,32d6,32d#6,32f6,16a#,16c6,a#,16a6,16d6.,16a#6,32a6,32a6,32g6,32f#6,32a6,8g6,16g6,16c6.,32a6,32a6,32g6,32g6,32f6,32e6,32g6,8f6,16f6,16a#.,16a#6,32g6,16f6,16a#.,16f6,32d#6,32d6,32d6,32d#6,32f6,16a#,16c6.,32d6,32d#6,32f6,16a#,16c6.,32d6,32d#6,32f6,16a#6,16c7,8a#.6")
        #self.load("topcat2:d=8,o=5,b=112:f,a#,16p,16f.,a#,16p,f,a#,16p,16f.,a#,16p,16f,16f,16f,16g,16g,16a,a#,a#,2p,16a#,a#,16g,a,16g,f,a#.,a#,2p,16a#,a#,16g,a,16g,f.,d.,d#.,e.,f.,16g.,16g#.,16a.,4a#.,p,c.6,c.6,c.6,c.6,16c.6,16a.,16g.,4f.,p,a#,a#,2p,16a#,a#,16g,a,16g,f.,a#,a#.,4c6,c6,4g.,4p,g,16a,a#.,g,16a,a#.,c6,16c#6,d")
        #self.load("williamt:d=4,o=5,b=140:16c,16c,16c,16p,16c,16c,16c,16p,16c,16c,16f,16p,8g,16a,16p,16c,16c,16c,16p,16c,16c,16f,16p,16a,16a,16g,16p,8e,16c,16p,16c,16c,16c,16p,16c,16c,16c,16p,16c,16c,16f,16p,8g,16a,16p,16f,16a,c6,16p,16a#,16a,16g,16f,16p,16a,16p,16f,16p")
        self.note = 0
        self.tick = Tick("rtttl", 333, False, False)
        #self.on = False
        #self.repeat = False
        #self.tune = ""
        #self.write_repeat = False
        #self.write_tune = ""
        # Play a tune
        #self.write(True, "friends1:d=8,o=5,b=90:b,16b,16a,16g,f,f,16g,a,4g,b,16b,16a,16g,f,f,16g,a,4g,4,6d,g,a,c6,b,a,g.,16g,d,g,a,2a,16d,g,a,c6,b,a,g.,16c6,b,a,g,2d6,16c6,c6,c6,c6,b,a,g.,16a,b,4b,16g,16a,16b,16c6,c6,c6,c6,c6,b,a,g,g.,16d,16g,16a,b,4a,4g,d,6,c6,4b,16a,g,b.,a")
        # Start initial idle timer
        #self.tick.write(333, False)

    # Load tune function
    def load(self, tune):
        print(f'Rtttl.load("{tune}")')
        # Assume invalid
        result = False
        # REmove spaces and convert to lower case
        tune = tune.replace(" ", "").lower()
        # Split on colons
        tune_parts = tune.split(":")
        tune_parts_count = len(tune_parts)
        print(f'tune_parts = {tune_parts}')
        # Got two parts ? 
        if tune_parts_count == 2 or tune_parts_count == 3: 
            # Extract name
            name = tune_parts[0]
            # Extract defaults
            duration = 4
            octave = 6
            bpm = 63                    
            notes_index = 1
            if tune_parts_count == 3:
                notes_index = 2
                defaults = tune_parts[1].split(",")
                for default in defaults:
                    # Default duration
                    index = default.find("d=")
                    if index == 0: 
                        value_str = default[index+2:]
                        print(f'd value_str = "{value_str}"')
                        print(f'{dir(value_str)}')
                        try:
                            value_int = int(value_str)
                            if value_int in [1, 2, 4, 8, 16, 32]:
                                duration = value_int
                        except:
                            pass
                    # Default octave
                    index = default.find("o=")
                    if index == 0: 
                        value_str = default[index+2:]
                        try:
                            value_int = int(value_str)
                            if value_int >= 4 and value_int <= 7:
                                octave = value_int 
                        except:
                            pass
                    # Default bpm
                    index = default.find("b=")
                    if index == 0: 
                        value_str = default[index+2:]
                        try:
                            value_int = int(value_str)
                            if value_int >= 25 and value_int <= 900:
                                bpm = value_int 
                        except:
                            pass
            # Calculate length of a whole note
            # Ensure a whole note is a multiple of a 32nd note
            whole_ms = (60000 * duration) // bpm
            whole_ms //= 32
            whole_ms *= 32
            # Debug data
            print(f'    name     = "{name}"')                                                                                              
            print(f'    duration = {duration}')
            print(f'    octave   = {octave}')
            print(f'    bpm      = {bpm}')        
            print(f'    whole_ms = {whole_ms}')            
            # Extract note data
            self.notes = []
            datas = tune_parts[notes_index].split(",")
            for data in datas:
                d_string = ""
                p_string = ""
                o_string = ""
                dot = False
                state = 0
                index = 0
                while index < len(data):
                    if state == 0: # Looking for duration (optional)
                        if data[index] in ["1", "2", "3", "4", "6", "8"]:
                            d_string += data[index]
                            index += 1
                        else:
                            state = 1
                    elif state == 1: # Looking for pitch note letter (mandatory)
                        if data[index] in ["a", "b", "c", "d", "e", "f", "g", "p"]:
                            p_string += data[index]
                            index += 1
                        else:
                            p_string += "p"
                        if p_string == "p":
                            state = 4
                        else:
                            state = 2
                    elif state == 2: # Looking for sharp (optional)
                        if data[index] == "#":
                            p_string += data[index]
                            index += 1
                        else:
                            state = 3
                    elif state == 3: # looking for octave or dot (optional - sometimes in different orders)
                        if data[index] in ["4", "5", "6", "7"]:
                            if len(o_string) == 0:
                                o_string += data[index]
                        elif data[index] == ".":
                            dot = True
                        index += 1                            
                    else:
                        index += 1

                if d_string not in ["1", "2", "4", "8", "16", "32"]:
                    d_string = str(duration)
                if o_string == "":
                    p_string += str(octave)
                else: 
                    p_string += o_string
                d_int = int(d_string)
                ms = whole_ms // d_int
                hz = 0
                if dot: ms += (ms//2)
                if p_string in self.frequencies:
                    hz = self.frequencies[p_string]
                self.notes.append((hz, ms))
                print(f'data="{data}", d="{d_string}", p="{p_string}", dot={dot}, ms={ms}, hz={hz}')

            print(f'    result   = {result}') 

    def main(self):
        if self.tick.read():
            if self.note < len(self.notes):
                piezo_on = True
                if self.notes[self.note][0] == 0:
                    piezo_on = False
                self.piezo.write(piezo_on, self.notes[self.note][0])
                self.tick.write(self.notes[self.note][1], False)
                self.note += 1
            else:
                self.piezo.write(False, 0)


# Rtttl class (END)




