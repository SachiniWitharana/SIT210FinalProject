import paho.mqtt.client as mqtt			# MQTT library
import RPi.GPIO as GPIO
import RPi.GPIO
import time					# time library
from time import sleep
#GUI#
from tkinter import *
import tkinter.font
from gpiozero import LED

RPi.GPIO.setmode(RPi.GPIO.BCM)
from gpiozero import LED  # import the LED library from the gpiozero
#buzzer implementations
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#Buzzer pin in 27
alarm_status = 0
buzz = 27

GPIO.setup(buzz,GPIO.OUT)

message = ""
### GUI IMPLEMENTATIONS  ###
win = Tk()
win.title("Home Alarm")
myFont = tkinter.font.Font(family = 'Helvetica', size = 16, weight = "bold")
### Event Function for Alarm on ###
def alarmOn():
    global alarm_status
    alarm_status = 1;
    
### Event Functions for Alarm off ###
def alarmOff():
    global alarm_status
    alarm_status = 0;
    GPIO.output(buzz,GPIO.LOW)
    print ("No Beep")
    sleep(0.5)
    
# Our "on message" event
def messageSent (client, userdata, message):
    message = str(message.payload.decode("utf-8"))
    topic = str(message.topic)
    global door_status
    door_status = message
    if door_status == "1" and alarm_status == 1:
        while alarm_status == 1:
            GPIO.output(buzz,GPIO.HIGH)
            print ("Beep")
            sleep(0.5) # delay
            GPIO.output(buzz,GPIO.LOW)
            print ("No Beep")
            sleep(0.5)
    else:
        GPIO.output(buzz,GPIO.LOW)
        print ("No Beep")
        sleep(0.5)

ourClient = mqtt.Client("makerio_mqtt")#client object
ourClient.connect("test.mosquitto.org", 1883)
ourClient.subscribe("argonLog")
ourClient.on_message = messageSent
ourClient.loop_start()#mqtt loop

def close():
    RPi.GPIO.cleanup()
    win.destroy()
    

### Button implementations for the GUI  ###

# Button trigger the selected LED 
alarmButtonO = Button(win, text='Turn on alarm', font=myFont, command=alarmOn, bg='blue', height=1, width=26)
alarmButtonO.grid(row=0,column=1)

alarmButtonF = Button(win, text='Turn off alarm', font=myFont, command=alarmOff, bg='red', height=1, width=26)
alarmButtonF.grid(row=2,column=1)

win.protocol("WM_DELETE_WINDOW" , close)

win.mainloop()




        


