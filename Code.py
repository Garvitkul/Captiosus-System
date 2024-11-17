#Importing all the required libraries

import RPi.GPIO as GPIO
from RPLCD.gpio import CharLCD
import MFRC522
import signal
import time
from time import sleep
import smtplib
import os


#Setting up the SMTP

s = smtplib.SMTP('smtp.gmail.com', 587)
s.starttls()
s.login("captiosus.system@gmail.com", "Captiosus@123")  
messagea = "Entry Detected- Permitted"  
messageb = "Entry Detected- Denied"
subject = "Captiosus Alert"
message1 = 'Subject:{}\n{}'.format(subject, messagea)
message2 = 'Subject:{}\n{}'.format(subject, messageb)

#Setting up GPIO pins

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
pwm=GPIO.PWM(11, 50)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(31, GPIO.OUT)
GPIO.setup(29, GPIO.OUT)
GPIO.setup(38, GPIO.OUT)
lcd = CharLCD(numbering_mode=GPIO.BOARD, cols=16, rows=2, pin_rs=37, pin_e=35, pins_data=[33, 31, 29, 38])
buzzer=26
led_n=32
led_r=36
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(led_n,GPIO.OUT)
GPIO.setup(led_r,GPIO.OUT)

#Creating a function for Not Recognised Event
 
def notrecognised():
     GPIO.output(led_n,GPIO.HIGH)
     GPIO.output(buzzer,GPIO.HIGH)
     os.system("espeak-ng 'Your entry is denied'")
     lcd.cursor_pos = (0, 2)
     lcd.write_string('Entry Denied')
     sleep(0.3)
     GPIO.output(buzzer,GPIO.LOW)
     sleep(0.3)
     GPIO.output(buzzer,GPIO.HIGH)
     sleep(0.3)
     GPIO.output(buzzer,GPIO.LOW)
     sleep(0.3)
     GPIO.output(buzzer,GPIO.HIGH)
     sleep(0.3)
     GPIO.output(buzzer,GPIO.LOW)
     sleep(0.3)
     GPIO.output(buzzer,GPIO.HIGH)
     sleep(0.3)
     GPIO.output(buzzer,GPIO.LOW)
     sleep(0.3)
     GPIO.output(buzzer,GPIO.HIGH)
     sleep(0.3)
     GPIO.output(buzzer,GPIO.LOW)
     sleep(0.3)
     GPIO.output(buzzer,GPIO.HIGH)
     sleep(0.3)
     GPIO.output(buzzer,GPIO.LOW)
     GPIO.output(led_n,GPIO.LOW)
     lcd.clear()

#Creating a function for Recognised Event

def recognised():
     GPIO.output(led_r,GPIO.HIGH)
     GPIO.output(buzzer,GPIO.HIGH)
     os.system("espeak-ng 'You are welcome, please wear mask before you enter the room'")
     pwm.start(0)
     pwm.ChangeDutyCycle(10)
     lcd.cursor_pos = (0, 0)
     lcd.write_string('You are Welcome')
     sleep(0.5)
     GPIO.output(buzzer,GPIO.LOW)
     sleep(2.5)
     GPIO.output(led_r,GPIO.LOW)
     lcd.clear()
     pwm.ChangeDutyCycle(7.5) # neutral position
     sleep(1)

continue_reading = True

# Capture SIGINT for cleanup when the script is aborted
def end_read(signal,frame):
    global continue_reading
    print ("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()
 
# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)
 
# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()
 
# Welcome message
print ("Welcome to the MFRC522 data read example")
print ("Press Ctrl-C to stop.")
 
# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:
    
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
        print ("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3])+','+str(uid[4]))  
        # This is the default key for authentication
        key = [0xFF,0xFF,0xFF,0xFF,0xFF,0xFF]
        
        # Select the scanned tag
        MIFAREReader.MFRC522_SelectTag(uid)
        
        #ENTER Your Card UID here (Registered database of RFIDs)
        my_uid = [178,2,40,49,169]
        
        
        #Check to see if card UID read matches your card UID
        if uid == my_uid:                #Open the Doggy Door if matching UIDs
            print("Access Granted")
            recognised()
            s.sendmail("captiosus.system@gmail.com", "garvit@gmail.com", message1)
        s.sendmail("captiosus.system@gmail.com", "shruti@gmail.com",message1)
            time.sleep(1)
            
        else:                            #Don't open if UIDs don't match
            print("Access Denied, YOU SHALL NOT PASS!")
            notrecognised()
        s.sendmail("captiosus.system@gmail.com", "garvitindian@gmail.com",message2)
            s.sendmail("captiosus.system@gmail.com", "shrutivij15@gmail.com",message2)
        time.sleep(1)
