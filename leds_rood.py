from shiftpi_rood import ALL, LOW, HIGH, digitalWrite
import RPi.GPIO as GPIO
import time


def baanRood(count_rood):
    print(count_rood)
    try:
        for i in range(0,count_rood):
            digitalWrite(i,HIGH)
            i = i + 1
    except KeyboardInterrupt:
        digitalWrite(ALL, LOW)
        pass
    finally:
        pass

def test(i):
    digitalWrite(ALL,LOW)
    x = 0
    while x < 1000:
        try:
            digitalWrite(i,HIGH)
            time.sleep(0.001)
            x = x + 1
        except KeyboardInterrupt:
            digitalWrite(ALL,LOW)
            pass
        finally:
            digitalWrite(ALL,LOW)
            pass

# test(ALL)