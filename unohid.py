#!/usr/bin/python
#originally written by https://github.com/ex0dus-0x/
import argparse
import serial
import serial.tools.list_ports
from os import system

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
        print "No Arduino found! If it is flashed, it will not be detected"
    else:
        ser = serial.Serial(arduino_ports[0])
        print "Arduino found! "

    if len(arduino_ports) > 1:
        print 'Multiple Arduinos found!'

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
