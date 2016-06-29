from opdrachten import Opdracht
from RPi import GPIO
from shiftpi_rood import ALL, LOW, digitalWrite, HIGH
from shiftpi_blauw import ALL as ALL2, LOW as LOW2, digitalWrite as digitalWrite2, HIGH as HIGH2
import subprocess
import rfidreader
import time
import buttons
from leds_blauw import baanBlauw
from leds_rood import baanRood
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

count_blauw = 0
count_rood = 0

GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#   start van spel
spelregels = "/home/pi/iipmedt-f/Python_code/sounds/spelregels.wav"

#   als er wat fout is
error = "/home/pi/iipmedt-f/Python_code/sounds/error.wav"

#   sensor opdracht
sensor = "/home/pi/iipmedt-f/Python_code/sounds/opdracht.wav"

#   quizvraag
quizvraag = "/home/pi/iipmedt-f/Python_code/sounds/quizvraag.wav"

#   goed of fout
Goed = "/home/pi/iipmedt-f/Python_code/sounds/Goed.wav"
goed_ping = "/home/pi/iipmedt-f/Python_code/sounds/goed_ping.wav"
Fout = "/home/pi/iipmedt-f/Python_code/sounds/Fout.wav"
fout_ping = "/home/pi/iipmedt-f/Python_code/sounds/fout_ping.wav"

#   begint na opdracht  goed of fout
feedback_6 = "/home/pi/iipmedt-f/Python_code/sounds/feedback_6.wav"
feedback_7 = "/home/pi/iipmedt-f/Python_code/sounds/feedback_7.wav"
feedback_8 = "/home/pi/iipmedt-f/Python_code/sounds/feedback_8.wav"
feedback_9 = "/home/pi/iipmedt-f/Python_code/sounds/feedback_9.wav"
feedback_10 = "/home/pi/iipmedt-f/Python_code/sounds/feedback_10.wav"
feedback_16 = "/home/pi/iipmedt-f/Python_code/sounds/feedback_16.wav"
feedback_17 = "/home/pi/iipmedt-f/Python_code/sounds/feedback_17.wav"
feedback_18 = "/home/pi/iipmedt-f/Python_code/sounds/feedback_18.wav"
feedback_19 = "/home/pi/iipmedt-f/Python_code/sounds/feedback_19.wav"
feedback_20 = "/home/pi/iipmedt-f/Python_code/sounds/feedback_20.wav"
feedback_hart = "/home/pi/iipmedt-f/Python_code/sounds/feedback_hart.wav"
feedback_hart2 = "/home/pi/iipmedt-f/Python_code/sounds/feedback_hart2.wav"
feedback_pink = "/home/pi/iipmedt-f/Python_code/sounds/feedback_pink.wav"
feedback_duim = "/home/pi/iipmedt-f/Python_code/sounds/feedback_duim.wav"
feedback_temp = "/home/pi/iipmedt-f/Python_code/sounds/feedback_temp.wav"

#   nadat er een antwoord is gegeven
blauw_kaart = "/home/pi/iipmedt-f/Python_code/sounds/blauw_kaart.wav"
rood_kaart = "/home/pi/iipmedt-f/Python_code/sounds/rood_kaart.wav"

#   als sensor vraag
hartslagsensor = "/home/pi/iipmedt-f/Python_code/sounds/hartslagsensor.wav"
temperatuursensor = "/home/pi/iipmedt-f/Python_code/sounds/temperatuursensor.wav"
druksensor_pink = "/home/pi/iipmedt-f/Python_code/sounds/druksensor_pink.wav"
druksensor_duim = "/home/pi/iipmedt-f/Python_code/sounds/druksensor_duim.wav"

#   als vraag al is geweest
opdracht_geweest = "/home/pi/iipmedt-f/Python_code/sounds/geweest.wav"

#   als speleinde
win_sound = "/home/pi/iipmedt-f/Python_code/sounds/win_sound.wav"
win_r = "/home/pi/iipmedt-f/Python_code/sounds/win_r.wav"
win_b = "/home/pi/iipmedt-f/Python_code/sounds/win_b.wav"
gelijkspel = "/home/pi/iipmedt-f/Python_code/sounds/gelijkspel.wav"
restart = "/home/pi/iipmedt-f/Python_code/sounds/restart.wav"

#   idle mode spel
startknop = "/home/pi/iipmedt-f/Python_code/sounds/start.wav"

def sound(sound):
    #   gebruik mplayer met volume +10dB
    command = "/usr/bin/mplayer " + sound + " -af volume=12"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]

    print(output)

#   reset voor debuggen
def reset_fast():
    time.sleep(2)
    digitalWrite2(ALL2,LOW2)
    time.sleep(0.4)
    digitalWrite(ALL,LOW)
    GPIO.cleanup()

#   reset voor het spel
def reset():
    sound(restart)
    time.sleep(20)
    digitalWrite2(ALL2,LOW2)
    time.sleep(0.4)
    digitalWrite(ALL,LOW)
    GPIO.cleanup()
    subprocess.call(['sudo reboot'], shell=True)


def goed():
    sound(Goed)


def fout():
    sound(Fout)

#   main functie
def run():
    print("GO")

    #   declareer global variabelen voor het tellen van de teamscore
    global count_rood
    global count_blauw

    #   forceer alle ledjes uit aan het begin van het spel
    if count_rood == 0 and count_blauw == 0:
        digitalWrite2(ALL2, LOW2)
        digitalWrite(ALL, LOW)

    #   initialiseer de rfid reader klasse
    rpi = rfidreader.RFID()

    #   initialiseer de Opdracht klasse
    opdr = Opdracht()

    # zet check voor spel einde op 0
    spelstop = 0

    try:

        spelstart = 0

        while spelstart == 0:
            sound(startknop)
            if buttons.button_groen() == True:
                spelstart = 1
            else:
                pass

        if spelstart == 1:
            sound(spelregels)
            sound(blauw_kaart)
            #   check voor spel einde
            while spelstop != 1:

                #   lees RFID reader uit
                lees = rpi.read()

                #   hele reeks aan checks voor de opdrachtstructuur
                #   zet de return uit de rpi.read() functie gelijk aan een opdracht
                #   en voert die opdracht uit

                #   opdrachten 1 - 5: Sensor opdrachten Team Blauw
                if lees == 1:
                    print ("opdracht 1")
                    sound(sensor)
                    sound(temperatuursensor)
                    # go()
                    # temperatuur = dingetje.runtemp()
                    # print(temperatuur)
                    if(opdr.runtemp()) >= 36.00:
                        count_blauw += 1
                        print(count_blauw)
                        baanBlauw(count_blauw)
                        sound(goed_ping)
                        goed()
                        sound(feedback_temp)
                        if count_blauw == 8:
                            pass
                        else:
                            sound(rood_kaart)
                    else:
                        sound(fout_ping)
                        fout()
                        sound(feedback_temp)
                        sound(rood_kaart)
                if lees == 2:
                    print ("opdracht 2")
                    sound(sensor)
                    sound(hartslagsensor)
                    # go()
                    if (opdr.runhart() >= 80):
                        count_blauw += 1
                        print(count_blauw)
                        baanBlauw(count_blauw)
                        sound(goed_ping)
                        goed()
                        sound(feedback_hart)
                        if count_blauw == 8:
                            pass
                        else:
                            sound(rood_kaart)
                    else:
                        sound(fout_ping)
                        fout()
                        sound(feedback_hart)
                        sound(rood_kaart)
                if lees == 3:
                    sound(sensor)
                    sound(hartslagsensor)
                    # go()
                    if (opdr.runhart()+10 >= 100):
                        count_blauw += 1
                        print(count_blauw)
                        baanBlauw(count_blauw)
                        sound(goed_ping)
                        goed()
                        sound(feedback_hart2)
                        if count_blauw == 8:
                            pass
                        else:
                            sound(rood_kaart)
                    else:
                        sound(fout_ping)
                        fout()
                        sound(feedback_hart2)
                        sound(rood_kaart)
                if lees == 4:
                    sound(sensor)
                    sound(druksensor_pink)
                    # go()
                    if (opdr.runforce() >= 750):
                        count_blauw += 1
                        print(count_blauw)
                        baanBlauw(count_blauw)
                        sound(goed_ping)
                        goed()
                        sound(feedback_pink)
                        if count_blauw == 8:
                            pass
                        else:
                            sound(rood_kaart)
                    else:
                        sound(fout_ping)
                        fout()
                        sound(feedback_pink)
                        sound(rood_kaart)
                if lees == 5:
                    sound(sensor)
                    sound(druksensor_duim)
                    # go()
                    if (opdr.runforce() >= 1500):
                        count_blauw += 1
                        print(count_blauw)
                        baanBlauw(count_blauw)
                        sound(goed_ping)
                        goed()
                        sound(feedback_duim)
                        if count_blauw == 8:
                            pass
                        else:
                            sound(rood_kaart)
                    else:
                        sound(fout_ping)
                        fout()
                        sound(feedback_duim)
                        sound(rood_kaart)

                #   opdrachten 6 - 10: Quizvragen Team Blauw
                if lees == 6:
                    print ("opdracht 6")
                    sound(quizvraag)
                    # go()
                    if(buttons.antwoord_button() == False):
                        count_blauw += 1
                        print(count_blauw)
                        baanBlauw(count_blauw)
                        sound(goed_ping)
                        goed()
                        sound(feedback_6)
                        if count_blauw == 8:
                            pass
                        else:
                            sound(rood_kaart)
                    else:
                        sound(fout_ping)
                        fout()
                        sound(feedback_6)
                        sound(rood_kaart)
                if lees == 7:
                    print ("opdracht 7")
                    sound(quizvraag)
                    # go()
                    if (buttons.antwoord_button() == True):
                        count_blauw += 1
                        print(count_blauw)
                        baanBlauw(count_blauw)
                        sound(goed_ping)
                        goed()
                        sound(feedback_7)
                        if count_blauw == 8:
                            pass
                        else:
                            sound(rood_kaart)
                    else:
                        sound(fout_ping)
                        fout()
                        sound(feedback_7)
                        sound(rood_kaart)
                if lees == 8:
                    sound(quizvraag)
                    # go()
                    if (buttons.antwoord_button() == True):
                        count_blauw += 1
                        print(count_blauw)
                        baanBlauw(count_blauw)
                        sound(goed_ping)
                        goed()
                        sound(feedback_8)
                        if count_blauw == 8:
                            pass
                        else:
                            sound(rood_kaart)
                    else:
                        sound(fout_ping)
                        fout()
                        sound(feedback_8)
                        sound(rood_kaart)
                if lees == 9:
                    sound(quizvraag)
                    # go()
                    if (buttons.antwoord_button() == False):
                        count_blauw += 1
                        print(count_blauw)
                        baanBlauw(count_blauw)
                        sound(goed_ping)
                        goed()
                        sound(feedback_9)
                        if count_blauw == 8:
                            pass
                        else:
                            sound(rood_kaart)
                    else:
                        sound(fout_ping)
                        fout()
                        sound(feedback_9)
                        sound(rood_kaart)
                if lees == 10:
                    sound(quizvraag)
                    # go()
                    if (buttons.antwoord_button() == False):
                        count_blauw += 1
                        print(count_blauw)
                        baanBlauw(count_blauw)
                        sound(goed_ping)
                        goed()
                        sound(feedback_10)
                        if count_blauw == 8:
                            pass
                        else:
                            sound(rood_kaart)
                    else:
                        sound(fout_ping)
                        fout()
                        sound(feedback_10)
                        sound(rood_kaart)

                #   opdrachten 11 - 15: Sensor opdrachten Team Rood
                if lees == 11:
                    print ("opdracht 11")
                    sound(sensor)
                    sound(hartslagsensor)
                    # go()
                    if opdr.runhart()+10 >= 100:
                        count_rood += 1
                        print(count_rood)
                        baanRood(count_rood)
                        sound(goed_ping)
                        goed()
                        sound(feedback_hart2)
                        if count_rood == 8:
                            pass
                        else:
                            sound(blauw_kaart)
                    else:
                        sound(fout_ping)
                        fout()
                        sound(feedback_hart2)
                        sound(blauw_kaart)
                if lees == 12:
                    print ("opdracht 12")
                    sound(sensor)
                    sound(temperatuursensor)
                    # go()
                    if (opdr.runtemp() >= 36):
                        count_rood += 1
                        print(count_rood)
                        baanRood(count_rood)
                        sound(goed_ping)
                        goed()
                        sound(feedback_temp)
                        if count_rood == 8:
                            pass
                        else:
                            sound(blauw_kaart)
                    else:
                        sound(fout_ping)
                        fout()
                        sound(feedback_temp)
                        sound(blauw_kaart)
                if lees == 13:
                    sound(sensor)
                    sound(druksensor_pink)
                    # go()
                    if (opdr.runforce() >= 750):
                        count_rood += 1
                        print(count_rood)
                        baanRood(count_rood)
                        sound(goed_ping)
                        goed()
                        sound(feedback_pink)
                        if count_rood == 8:
                            pass
                        else:
                            sound(blauw_kaart)
                    else:
                        sound(fout_ping)
                        fout()
                        sound(feedback_pink)
                        sound(blauw_kaart)
                if lees == 14:
                    sound(sensor)
                    sound(druksensor_duim)
                    # go()
                    if (opdr.runforce() >= 1500):
                        count_rood += 1
                        print(count_rood)
                        baanRood(count_rood)
                        sound(goed_ping)
                        goed()
                        sound(feedback_duim)
                        if count_rood == 8:
                            pass
                        else:
                            sound(blauw_kaart)
                    else:
                        sound(fout_ping)
                        fout()
                        sound(feedback_duim)
                        sound(blauw_kaart)
                if lees == 15:
                    sound(sensor)
                    sound(hartslagsensor)
                    # go()
                    if (opdr.runhart() >= 80):
                        count_rood += 1
                        print(count_rood)
                        baanRood(count_rood)
                        sound(goed_ping)
                        goed()
                        sound(feedback_hart)
                        if count_rood == 8:
                            pass
                        else:
                            sound(blauw_kaart)
                    else:
                        sound(fout_ping)
                        fout()
                        sound(feedback_hart)
                        sound(blauw_kaart)

                #   opdrachten 16 - 20: Quizvragen Team Rood
                if lees == 16:
                    print ("opdracht 16")
                    sound(quizvraag)
                    # go()
                    if (buttons.antwoord_button() == False):
                        count_rood += 1
                        print(count_rood)
                        baanRood(count_rood)
                        sound(goed_ping)
                        goed()
                        sound(feedback_16)
                        if count_rood == 8:
                            pass
                        else:
                            sound(blauw_kaart)
                    else:
                        sound(fout_ping)
                        fout()
                        sound(feedback_16)
                        sound(blauw_kaart)
                if lees == 17:
                    print ("opdracht 17")
                    sound(quizvraag)
                    # go()
                    if (buttons.antwoord_button() == True):
                        count_rood += 1
                        print(count_rood)
                        baanRood(count_rood)
                        sound(goed_ping)
                        goed()
                        sound(feedback_17)
                        if count_rood == 8:
                            pass
                        else:
                            sound(blauw_kaart)
                    else:
                        sound(fout_ping)
                        fout()
                        sound(feedback_17)
                        sound(blauw_kaart)
                if lees == 18:
                    sound(quizvraag)
                    # go()
                    if (buttons.antwoord_button() == False):
                        count_rood += 1
                        print(count_rood)
                        baanRood(count_rood)
                        sound(goed_ping)
                        goed()
                        sound(feedback_18)
                        if count_rood == 8:
                            pass
                        else:
                            sound(blauw_kaart)
                    else:
                        sound(fout_ping)
                        fout()
                        sound(feedback_18)
                        sound(blauw_kaart)
                if lees == 19:
                    sound(quizvraag)
                    # go()
                    if (buttons.antwoord_button() == False):
                        count_rood += 1
                        print(count_rood)
                        baanRood(count_rood)
                        sound(goed_ping)
                        goed()
                        sound(feedback_19)
                        if count_rood == 8:
                            pass
                        else:
                            sound(blauw_kaart)
                    else:
                        sound(fout_ping)
                        fout()
                        sound(feedback_19)
                        sound(blauw_kaart)
                if lees == 20:
                    sound(quizvraag)
                    # go()
                    if (buttons.antwoord_button() == False):
                        count_rood += 1
                        print(count_rood)
                        baanRood(count_rood)
                        sound(goed_ping)
                        goed()
                        sound(feedback_20)
                        if count_rood == 8:
                            pass
                        else:
                            sound(blauw_kaart)
                    else:
                        sound(fout_ping)
                        fout()
                        sound(feedback_20)
                        sound(blauw_kaart)

                #   Als opdracht al geweest is, geeft rfid.read() de waarde 0 terug
                #   Hier word de audio feedback toegekend
                if lees == 0:
                    sound(opdracht_geweest)

                if lees == 50:
                    spelstop = 1

                #   Reset voorwaarde: alletwee de arcade knoppen indrukken en 5 seconden ingedrukt houden
                if GPIO.input(12) == 0 and GPIO.input(27) == 0:
                    time.sleep(5)
                    if GPIO.input(12) == 0 and GPIO.input(27) == 0:
                        reset()

                #   Als een team 8 punten heeft behaald, eindigt het spel
                if count_blauw == 8 or count_rood == 8:
                    if count_blauw == 8:
                        sound(win_sound)
                        sound(win_b)
                    else:
                        sound(win_sound)
                        sound(win_r)
                    spelstop = 1

                #   Als alle vragen geweest zijn
                if rpi.vr1 == True and rpi.vr2 == True and rpi.vr3 == True and rpi.vr4 == True and rpi.vr5 == True and rpi.vr6 == True and rpi.vr7 == True and rpi.vr8 == True and rpi.vr9 == True and rpi.vr10 == True and rpi.vr11 == True and rpi.vr12 == True and rpi.vr13 == True and rpi.vr14 == True and rpi.vr15 == True and rpi.vr16 == True and rpi.vr17 == True and rpi.vr18 == True and rpi.vr19 == True and rpi.vr20 == True:
                    rpi.opdracht = 21
                    rpi.continue_reading = False
                    #   en het gelijkspel is
                    if count_blauw == count_rood:
                        sound(win_sound)
                        sound(gelijkspel)
                    #   team blauw meer punten
                    elif count_blauw > count_rood:
                        sound(win_sound)
                        sound(win_b)
                    #   team rood meer punten
                    elif count_rood > count_blauw:
                        sound(win_sound)
                        sound(win_r)
                    spelstop = 1
                #   Anders, wacht op een opdracht
                else:
                    time.sleep(1)
                    print("wacht op opdracht")

    except KeyboardInterrupt:
        reset_fast()
    finally:
        reset()

run()