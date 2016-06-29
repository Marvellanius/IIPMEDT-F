from RPi import GPIO
import time
import serial
from random import randint
import layout
import smbus

#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

DEVICE = 0x20  # Device address (A0-A2)
IODIRA = 0x00  # Pin direction register
GPIOA = 0x12  # Register for inputs
GPPUA = 0x0C
IOPOLA = 0x02
IODIRB = 0X01
GPIOB = 0X13
GPPUB = 0X0D
OLATB = 0x15
OLATA = 0x14

# GPPUB = 0x0D

# Set first 7 GPA pins as outputs and
# last one as input.
bus.write_byte_data(DEVICE, IODIRA, 0x00)
bus.write_byte_data(DEVICE, GPIOA, 0)
# bus.write_byte_data(DEVICE, GPPUA, 0xFF)
# bus.write_byte_data(DEVICE, IOPOLA, 0xFF)
bus.write_byte_data(DEVICE, IODIRB, 0x00)
bus.write_byte_data(DEVICE, GPIOB, 0)

ser = serial.Serial('/dev/ttyUSB0', 9600)

class Hartsensor(object):
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
    @property
    def opdrachten(self):
        try:
            e = 0
            avghart = 0
            while e < 10:
                # ser.flushInput()
                # ser.flushOutput()
                # ser.write('1')
                # hartslag = ser.readline()
                hartslag = randint(90,110)
                print(hartslag)
                avghart = avghart + float(hartslag)

                s = str(hartslag)
                num = {' ': 0b11111111,
                    '0': 0b11000000,
                    '1': 0b11111001,
                    '2': 0b10010100,
                    '3': 0b10110000,
                    '4': 0b10101001,
                    '5': 0b10100010, # (0, 1, 0, 0, 1, 0, 0, 1),
                    '6': 0b10000010, # (0, 1, 0, 0, 0, 0, 0, 1),
                    '7': 0b11111000, # (0, 0, 0, 1, 1, 1, 1, 1),
                    '8': 0b10000000, #(0, 0, 0, 0, 0, 0, 0, 1),
                    '9': 0b10100000, # (0, 0, 0, 0, 1, 0, 0, 1),
                    '.': 0b10000011, # (1, 1, 0, 0, 0, 0, 0, 1),
                    'G': 0b11000010, # (0, 1, 0, 0, 0, 0, 1, 1),
                    'O': 0b11000000, #(0, 0, 0, 0, 0, 0, 1, 1),
                    'o': 0b10010011, #(1, 1, 0, 0, 0, 1, 0, 1),
                    'D': 0b10010001, #(1, 0, 0, 0, 0, 1, 0, 1),
                    'F': 0b10001110, #(0, 1, 1, 1, 0, 0, 0, 1),
                    'u': 0b11010011, #(1, 1, 0, 0, 0, 1, 1, 1),
                    't': 0b10000111, #(1, 1, 1, 0, 0, 0, 0, 1),
                    'y': 0b10010001, #(1, 0, 0, 0, 1, 0, 0, 1),
                    'E': 0b10000110, #(0, 1, 1, 0, 0, 0, 0, 1),
                    'A': 0b10001000, #(0, 0, 0, 1, 0, 0, 0, 1),
                    'L': 0b11000111, #(1, 1, 1, 0, 0, 0, 1, 1),
                    'X': 0b10001001} #(1, 0, 0, 1, 0, 0, 0, 1)}
                display_string = (" "+s)

                x = 0
                while x < 200:
                    for digit in range(4):
                        if  (len(s) == 2):
                            display_string = ("  " + s)
                        elif (len(s) == 3):
                            display_string = (" " + s)
                        else:
                            display_string = ("Fout")
                    for digit in range(4):
                        bus.write_byte_data(DEVICE, OLATA, num[display_string[digit]])
                        # GPIO.output(segments, (num[display_string[digit]]))
                        if digit == 0:
                            bus.write_byte_data(DEVICE, OLATB, 0b00000001)
                        elif digit == 1:
                            bus.write_byte_data(DEVICE,OLATB,0b00000010)
                        elif digit == 2:
                            bus.write_byte_data(DEVICE,OLATB,0b00000100)
                        else:
                            bus.write_byte_data(DEVICE,OLATB,0b00001000)
                        # GPIO.output(digits[digit], 1)
                        time.sleep(0.001)
                        bus.write_byte_data(DEVICE, OLATB, 0)
                        # GPIO.output(digits[digit], 0)
                    x = x + 1
                e = e + 1
                ser.write('0')
            print ("avg: " + str(avghart/10))
            return avghart/10

        except KeyboardInterrupt:
            pass

        finally:
            pass