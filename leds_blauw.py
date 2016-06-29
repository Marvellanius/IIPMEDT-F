from shiftpi_blauw import ALL, LOW, HIGH, digitalWrite
import RPi.GPIO as GPIO
import time


def baanBlauw(count_blauw):
    print(count_blauw)
    try:
        for i in range(0,count_blauw):
            digitalWrite(i,HIGH)
            i = i + 1
    except KeyboardInterrupt:
        digitalWrite(ALL,LOW)
        pass
    finally:
        pass

def test(i):
    x = 0
    while x < 1000:
        try:
            digitalWrite(i,HIGH)
            x = x + 1
        except KeyboardInterrupt:
            pass
        finally:
            digitalWrite(ALL,LOW)

# test(ALL)
