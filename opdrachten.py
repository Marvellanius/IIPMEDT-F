from RPi import GPIO
import time
import force_sensor as force
import temp_sensor as temp
import hart_sensor as hart
import rfidreader as port

class Opdracht(object):

    opdracht = port.RFID()
    kracht = force.Forcesensor()
    temperatuur = temp.Tempsensor()
    hart = hart.Hartsensor()

    def runforce(self):
        force = self.kracht.opdrachten
        # kracht uitlezen
        try:
            return int(force)

        except KeyboardInterrupt:
            pass

        finally:
            print("next opdracht")


    # hartslagsensor
    def runhart(self):
        hartslag = self.hart.opdrachten
        # kracht uitlezen
        try:
            return hartslag
        except KeyboardInterrupt:
            pass

        finally:
            print("next opdracht")


    # temperatuursensor
    def runtemp(self):
        temp = self.temperatuur.opdrachten
        try:
            return temp
        except KeyboardInterrupt:
            pass
        finally:
            print("next opdracht")


