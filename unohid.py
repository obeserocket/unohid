#!/usr/bin/python
#originally written by https://github.com/ex0dus-0x/
import argparse
import serial
import serial.tools.list_ports
from os import system

#declare some colors to work with
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

# Instantiate ArgumentParser
parser = argparse.ArgumentParser(description='Hacking with the Arduino Uno')
parser.add_argument('--flash', '-f', action="store_true",
    help='Flash with HID firmware')
parser.add_argument('--unflash', '-uf', action="store_true",
    help='Flash with default firmware')
parser.add_argument('--detect', '-d', action="store_true",
    help='Detects whether a default arduino is plugged in')


# Parse arguments
args = parser.parse_args()

# Detect Arduino (as serial device)
if args.detect:
    arduino_ports = [
        p.device
        for p in serial.tools.list_ports.comports()
        if 'Arduino' in p.description
    ]

    if not arduino_ports:
        print bcolors.WARNING + "No Arduino found! If it is flashed, it will not be detected" + bcolors.ENDC
    else:
        ser = serial.Serial(arduino_ports[0])
        print bcolors.OKGREEN + "Arduino found! " + bcolors.ENDC

    if len(arduino_ports) > 1:
        print bcolors.OKBLUE + 'Multiple Arduinos found!' + bcolors.ENDC

# Flash as HID
elif args.flash:
    print "Please short GND and ICSP header pins. Press Enter to continue when complete."
    raw_input()
    system("dfu-programmer atmega16u2 erase")
    system("dfu-programmer atmega16u2 flash --debug 1 hex/Arduino-keyboard.hex")
    system("dfu-programmer atmega16u2 reset")
    print "Done! Arduino is now in HID mode\n"

# Flash as a regular serial device
elif args.unflash:
    print "Please short GND and ICSP header pins. Press Enter to continue when complete."
    raw_input()
    system("dfu-programmer atmega16u2 erase")
    system("dfu-programmer atmega16u2 flash --debug 1 hex/Arduino-usbserial.hex")
    system("dfu-programmer atmega16u2 reset")
    print "Done! Arduino is back to default mode\n"

# Print default help if none provided
else:
    print parser.print_help()
