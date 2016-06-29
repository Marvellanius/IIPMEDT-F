import signal
import MFRC522
import time


class RFID(object):
    vr1 = False
    vr2 = False
    vr3 = False
    vr4 = False
    vr5 = False
    vr6 = False
    vr7 = False
    vr8 = False
    vr9 = False
    vr10 = False
    vr11 = False
    vr12 = False
    vr13 = False
    vr14 = False
    vr15 = False
    vr16 = False
    vr17 = False
    vr18 = False
    vr19 = False
    vr20 = False
    opdracht = 0

    # Hook the SIGINT
    def read(self):
        continue_reading = True
        # Capture SIGINT for cleanup when the script is aborted
        # def end_read(signal,frame):
        #     global continue_reading
        #     print "Ctrl+C captured, ending read."
        #     continue_reading = False
        #     GPIO.cleanup()
        #
        # signal.signal(signal.SIGINT, end_read)

        # Create an object of the class MFRC522
        MIFAREReader = MFRC522.MFRC522()



        # Welcome message
        self.opdracht = 0
        # This loop keeps checking for chips. If one is near it will get the UID and authenticate
        while continue_reading:
            try:
                time.sleep(1)
                # Scan for cards
                (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    
                # If a card is found
                if status == MIFAREReader.MI_OK:
                    print ("Card detected")
    
                # Get the UID of the card
                (status,uid) = MIFAREReader.MFRC522_Anticoll()
    
                # If we have the UID, continue
                if status == MIFAREReader.MI_OK:
    
                    # Print UID
                    print ("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])+","+str(uid[4]))
                    
                    if uid == [136,4,157,19,2] and self.vr1 == False:
                        self.opdracht = 1
                        self.continue_reading = False
                        self.vr1 = True

                    elif uid == [136,4,156,19,3] and self.vr2 == False:
                        self.opdracht = 2
                        self.continue_reading = False
                        self.vr2 = True

                    elif uid == [136,4,178,187,133] and self.vr3 == False:
                        self.opdracht = 3
                        self.continue_reading = False
                        self.vr3 = True

                    elif uid == [136,4,178,182,136] and self.vr4 == False:
                        self.opdracht = 4
                        self.continue_reading = False
                        self.vr4 = True

                    elif uid == [136,4,178,199,249] and self.vr5 == False:
                        self.opdracht = 5
                        self.continue_reading = False
                        self.vr5 = True

                    elif uid == [136,4,178,187,133] and self.vr3 == False:
                        self.opdracht = 3
                        self.continue_reading = False
                        self.vr3 = True


                    elif uid == [136,4,155,19,4]and self.vr6 == False:
                        self.opdracht = 6
                        self.continue_reading = False
                        self.vr6 = True
                        
                    elif uid == [136,4,154,19,5] and self.vr7 == False:
                        self.opdracht = 7
                        self.continue_reading = False
                        self.vr7 = True

                    elif uid == [136,4,178,174,144] and self.vr8 == False:
                        self.opdracht = 8
                        self.continue_reading = False
                        self.vr8 = True

                    elif uid == [136,4,178,178,140] and self.vr9 == False:
                        self.opdracht = 9
                        self.continue_reading = False
                        self.vr9 = True

                    elif uid == [136,4,178,166,152] and self.vr10 == False:
                        self.opdracht = 10
                        self.continue_reading = False
                        self.vr10 = True

                    elif uid == [136,4,153,19,6] and self.vr11 == False:
                        self.opdracht = 11
                        self.continue_reading = False
                        self.vr11 = True
                        
                    elif uid == [136,4,162,19,61] and self.vr12 == False:
                        self.opdracht = 12
                        self.continue_reading = False
                        self.vr12 = True

                    elif uid == [136,4,178,68,122] and self.vr13 == False:
                        self.opdracht = 13
                        self.continue_reading = False
                        self.vr13 = True

                    elif uid == [136,4,178,170,148] and self.vr14 == False:
                        self.opdracht = 14
                        self.continue_reading = False
                        self.vr14 = True

                    elif uid == [136,4,178,191,129] and self.vr15 == False:
                        self.opdracht = 15
                        self.continue_reading = False
                        self.vr15 = True

                    elif uid == [136,4,161,19,62] and self.vr16 == False:
                        self.opdracht = 16
                        self.continue_reading = False
                        self.vr16 = True

                    elif uid == [136,4,160,19,63] and self.vr17 == False:
                        self.opdracht = 17
                        self.continue_reading = False
                        self.vr17 = True

                    elif uid == [136,4,177,224,221] and self.vr18 == False:
                        self.opdracht = 18
                        self.continue_reading = False
                        self.vr18 = True

                    elif uid == [136,4,177,196,249] and self.vr19 == False:
                        self.opdracht = 19
                        self.continue_reading = False
                        self.vr19 = True

                    elif uid == [136,4,178,195,253] and self.vr20 == False:
                        self.opdracht = 20
                        self.continue_reading = False
                        self.vr20 = True

                    elif uid == [136,4,177,232,213]:
                        self.opdracht = 50
                    # if self.vr1 == True and self.vr2 == True and self.vr3 == True and self.vr4 == True and self.vr5 == True and self.vr6 == True and self.vr7 == True and self.vr8 == True and self.vr9 == True and self.vr10 == True and self.vr11 == True and self.vr12 == True and self.vr13 == True and self.vr14 == True and self.vr15 == True and self.vr16 == True and self.vr17 == True and self.vr18 == True and self.vr19 == True and self.vr20 == True:
                    #     self.opdracht = 21
                    #     self.continue_reading = False
                    else:
                        print ("nix!")
                    print (self.opdracht)
                    return self.opdracht
            except KeyboardInterrupt:
                pass
            finally:
                pass
        
