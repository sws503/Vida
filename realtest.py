#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Example 5: Dialog - queryByText"""

from __future__ import print_function
import grpc
import user_auth as UA
import gigagenieRPC_pb2
import gigagenieRPC_pb2_grpc
import os
import RPi.GPIO as GPIO
import time
import Adafruit_DHT
from signal import signal, alarm, SIGALRM
signal(SIGALRM, lambda x:1/0)


HOST = 'gate.gigagenie.ai'
PORT = 4080

# DIALOG : queryByText
def queryByText(text):

	channel = grpc.secure_channel('{}:{}'.format(HOST, PORT), UA.getCredentials())
	stub = gigagenieRPC_pb2_grpc.GigagenieStub(channel)

	message = gigagenieRPC_pb2.reqQueryText()
	message.queryText = text
	message.userSession = "1234"
	message.deviceId = "yourdevice"
		
	response = stub.queryByText(message)

	print ("\n\nresultCd: %d" % (response.resultCd))
	if response.resultCd == 200:
		print ("\n\n\n질의한 내용: %s" % (response.uword))
		#dssAction = response.action
		for a in response.action:
			response = a.mesg
		parsing_resp = response.replace('<![CDATA[', '')
		parsing_resp = parsing_resp.replace(']]>', '')
		print("\n\n질의에 대한 답변: " + parsing_resp + '\n\n\n')
		#return response.url
	else:
            print ("Fail: %d" % (response.resultCd))
		#return None	 

def rc_time (pin_to_circuit):
    count = 0
  
    #Output on the pin for 
    GPIO.setup(pin_to_circuit, GPIO.OUT)
    GPIO.output(pin_to_circuit, GPIO.LOW)
    time.sleep(0.1)

    #Change the pin back to input
    GPIO.setup(pin_to_circuit, GPIO.IN)
  
    #Count until the pin goes high
    while (GPIO.input(pin_to_circuit) == GPIO.LOW):
        count += 1

    return count

def main():
        pin_temp = 2
        pin_distance = 3
        pin_light = 4

        sensor = Adafruit_DHT.DHT11
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin_distance, GPIO.IN)
        #humidity, temperature = Adafruit_DHT.read_retry(sensor, pin_temp)
        human = 0
        fl = 0
        while(True): 
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin_temp)
            if humidity is not None and temperature is not None:
                print ("Temp={0:0.1f}*C Humidity={1:0.1f}%".format(temperature, humidity))
            else:
                print ("Failed to get reading.")
            print("distance " + str(GPIO.input(pin_distance)))
            print("light " + str(rc_time(pin_light)))
            
            human += int(GPIO.input(pin_distance) == 0)
            print("human " + str(human))
            
            if(human >= 3):
                while(True):
                    print("유진님 집에 돌아오셨네용 오늘 하루는 어떠셨어요?")
                    #time = 10
                    try:
                        alarm(10)
                        x = input("type command ")
                        #time = 10
                        queryByText(x)
                    except TypeError:
                        human = 0
                        print("timed out")
                        break
            time.sleep(1)
	# Dialog : queryByText
        # x = input()
        # queryByText(x)

if __name__ == '__main__':
	main()
