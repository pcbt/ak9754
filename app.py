
import commands
import RPi.GPIO as GPIO
import time, threading
import paho.mqtt.client as mqtt
import AK9754 as ak

client = mqtt.Client()

def on_message(client, userdata, message):
    print str(message.payload.decode("utf-8"))
    if message.payload.decode("utf-8") == "0":
	client.publish("ak9754/givestatus", "Connected and working")

def power_up():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(12, GPIO.OUT)
    GPIO.output(12, False)
    GPIO.output(11, True)
    time.sleep(3)
    GPIO.output(11, False)
    GPIO.cleanup()

def start_module():
    ppp = commands.getstatusoutput('sudo pon internet2')


def control_module():
    cmd = commands.getstatusoutput('ifconfig ppp0')
    if cmd[0] != 0:
	print "Problem!!"
	client.loop_stop()
        start_module()
        time.sleep(30)
        control_module()
	print "Problem Solved!!"
	return 1
    else:
	return 0

def periodic_control():
    if control_module():
	client.connect("testserver.airchip.com.tr")
    print client.subscribe("ak9754/getstatus", qos = 1)
    client.on_message = on_message
    seatD=ak.readData()
    if seatD==0:
        ak.init_cont()
        time.sleep(2)
        print "sensor initialized"
    seatD=ak.readData()
    tempD=ak.readCData()
    data="Seat Data: "+str(seatD)+"\tTemperature Data: "+str(tempD)
    print data
    client.publish("ak9754/test", data)
    client.loop_start()
    threading.Timer(10,periodic_control).start()
    print "Periodic data sent!!"


commands.getstatusoutput('sudo poff internet2')
power_up()
time.sleep(12)
ak.init_cont()
periodic_control()
