import os
import RPi.GPIO as GPIO
from time import sleep

in1 = 24
in2 = 23
en = 25
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)

GPIO.output(in1, GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)

p.start(15)
temp=0
temp1=0

def measure_temp():
        temp=os.popen("vcgencmd measure_temp").readline()
        return (temp.replace("temp=","").replace("'C\n",""))

while(1):
       
	temp1=measure_temp()
	temp2=float(temp1)
	print(temp2)
        if 35>temp2>30:
                print("run")
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
        elif 40>temp2>35:
		GPIO.output(in1,GPIO.HIGH)
		GPIO.output(in2,GPIO.LOW)
                p.ChangeDutyCycle(50)
        elif temp2>40:
		GPIO.output(in1,GPIO.HIGH)
		GPIO.output(in2,GPIO.LOW)
                p.ChangeDutyCycle(80)
	sleep(3)
GPIO.cleanup()
