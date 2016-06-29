import RPi.GPIO as GPIO
import time

def button_rood():
    pin = 21

    prev_state = 1

    try:
        i = 0
        while i != 1:
            curr_state = GPIO.input(pin)

            if (curr_state != prev_state):
                if (curr_state == 0):
                    buttonRood = True
                    i = i + 1
                pass
    except KeyboardInterrupt:
        pass
    finally:
        return buttonRood


def button_groen():
    pin = 27
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    prev_state = 1
    buttonGroen = False
    try:
        i = 0
        while i != 1:
            # print "hi"
            curr_state = GPIO.input(pin)
            buttonGroen = False
            # print (curr_state)
            if (curr_state != prev_state):
                if (curr_state == 0):
                    buttonGroen = True
                    i = i + 1
    except KeyboardInterrupt:
        pass
    finally:
        return buttonGroen



def antwoord_button():
    buttonPin = 12
    buttonPin2 = 27

    prev_state = 1

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(buttonPin2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    try:
        i = 0
        while i != 1:
            curr_state = GPIO.input(buttonPin) # rood
            curr_state2 = GPIO.input(buttonPin2) # groen

            if (curr_state != prev_state):
                if (curr_state == 0):
                    event = False
                    i = i + 1
                pass
            elif (curr_state2 == 0):
                event = True
                i = i + 1
                pass
    except KeyboardInterrupt:
        pass
    finally:
        return event
        pass

