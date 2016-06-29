from RPi import GPIO
import time
import smbus

#   initialiseer de port expander pins
#bus = smbus.SMBus(0)  # Rev 1 Pi uses 0
bus = smbus.SMBus(1) # Rev 2 Pi uses 1

DEVICE = 0x20  # Device address (A0-A2)
IODIRA = 0x00  # Pin direction register
GPIOA = 0x12  # Register for inputs
OLATA = 0x14  # output register A
IODIRB = 0X01  # Pin direction register
GPIOB = 0X13  # Register for inputs
OLATB = 0x15  # output register B


#   zet de correcte registers aan op de port expander
#   allemaal als output tbv 7-segment display
#   initieer ze op 0
bus.write_byte_data(DEVICE, IODIRA, 0x00)
bus.write_byte_data(DEVICE, GPIOA, 0)
bus.write_byte_data(DEVICE, IODIRB, 0x00)
bus.write_byte_data(DEVICE, GPIOB, 0)


class Tempsensor(object):
    s = ""
    def __init__(self):
        GPIO.setmode(GPIO.BCM)

    #def seg(self):

    @property
    def opdrachten(self):
        try:
            # Definieer een array (temp).
            i = 0
            while i < 10:
                temp = {}
                sensorids = ["28-0115906b1bff"]
                # loop net zo lang alles sensors af dat in het array hieboven staan.
                for sensor in range(len(sensorids)):
                    tfile = open("/sys/bus/w1/devices/" + sensorids[sensor] + "/w1_slave")
                    # Lees alle dat uit het "bestand" in een variabele.
                    text = tfile.read()
                    # Sluit het "bestand" nadat we het gelezen hebben.
                    tfile.close()
                    # We gaan nu de tekst splitsen per nieuwe regel (\n)
                    # en we selecteren de 2e regel [1] (1e regel = [0])
                    secondline = text.split("\n")[1]
                    # Splits de regel in "woorden", er wordt gespleten op de spaties.
                    # We selecteren hier het 10 "woord" [9] (tellend vanaf 0)
                    temperaturedata = secondline.split(" ")[9]
                    # De eerste 2 karakters zijn "t=", deze moeten we weghalen.
                    # we maken meteen van de string een integer (nummer).
                    temperature = float(temperaturedata[2:])
                    # De temperatuurwaarde moeten we delen door 1000 voor de juiste waarde.
                    temp[sensor] = temperature / 1000
                    # print de gegevens naar de console.
                    print("l")
                    def temp1():
                        while True:
                            return temp[sensor]+9
                print(temp1())
                # temp1 = temp[sensor]
                s = str(temp1()).rjust(4)
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

                display_string = ("  " + s)
                x = 0
                print (len(s))
                while x < 200:
                    # for digit in range(4):
                    #     if (len(s) == 2):
                    #         display_string = (s)
                    #     elif (len(s) == 3):
                    #         display_string = (" " + s)
                    #     elif (len(s) == 6):
                    #         display_string = ("  " + s)
                    #     elif (len(s) == 1):
                    #         display_string = ("   " + s)
                    #     else:
                    #         display_string = ("Fout")

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
                i = i + 1
            return temp1()

        except KeyboardInterrupt:
            pass

        finally:
            pass




