#system developed for LPSMC YPEC 2016
#by Kwan King Hong Paros (paroskwan@gmail.com)
#date 18/5/2016


########################
# import library needed
import picamera
import datetime
import time
from itertools import cycle
from flask import Flask, render_template
from flask_socketio import SocketIO,emit
import json
import os
import RPi.GPIO as GPIO
import Adafruit_DHT
# import library needed
########################

########################
# GPIO pin setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
led_pin = 18
air_con_1_pin = 23
air_con_2_pin = 24
curtain_1_pin = 20
curtain_2_pin = 21
camera_pin = 27 
light_sensor_pin = 4
temp_sensor_pin = 17

GPIO.setup(led_pin,GPIO.OUT)
GPIO.setup(air_con_1_pin,GPIO.OUT)
GPIO.setup(air_con_2_pin,GPIO.OUT)
GPIO.setup(curtain_1_pin,GPIO.OUT)
GPIO.setup(curtain_2_pin,GPIO.OUT)
GPIO.setup(camera_pin,GPIO.OUT)
GPIO.setup(light_sensor_pin,GPIO.IN)
pwm_1 = GPIO.PWM(curtain_1_pin,50)
pwm_2 = GPIO.PWM(curtain_2_pin,50)

#temp sensor 
sensor = Adafruit_DHT.DHT22

#GPIO pin set up 
########################

########################
# client request list
full_automation = 0
led_on =  111
led_off = 110
air_con_1_on  = 211
air_con_1_off = 210
air_con_2_on  = 221
air_con_2_off = 220
curtain_1_on = 311
curtain_1_off = 310
curtain_2_on = 321
curtain_2_off = 320
camera_take_photo = 411
light_sensor_read = 511
temp_sensor_read  = 521
#client request list
########################


# main program
app = Flask(__name__)
app.config['SECERT_KET']='secret!'
socketio = SocketIO(app)

#render different html at different path
@app.route('/')
def index():
    return render_template('newindex.html')
@app.route('/automated')
def automated():
    return render_template('newauto.html')
@app.route('/manual')
def manual():
    return render_template('newmanual.html')
@app.route('/photo')
def photo():
    s = os.listdir("/home/pi/Desktop/YPEC/static/img")
    return render_template('photos.html',s = s)

# listening incoming message on channel 'client message'
@socketio.on('client_message')
def handle_client_message(message):
    client_message = json.loads(message)
    request = client_message["request"]
    print(client_message) # output in terminal for debug
    
    if (request == full_automation):
        #automated code 
        light_env = GPIO.input(light_sensor_pin)
        if (light_env == 0 ):

            condition = 'bright'
            GPIO.output(led_pin,GPIO.LOW)
            pwm_1 = GPIO.PWM(curtain_1_pin,50)
            pwm_2 = GPIO.PWM(curtain_2_pin,50)
            pwm_1.start(3)
            pwm_2.start(3)
            
            pwm_1.ChangeDutyCycle(3)
            pwm_2.ChangeDutyCycle(3)
            time.sleep(0.2)
            pwm_1.stop()
            pwm_2.stop()
        else :
            condition = 'dim'
            GPIO.output(led_pin,GPIO.HIGH)
            pwm_1 = GPIO.PWM(curtain_1_pin,50)
            pwm_2 = GPIO.PWM(curtain_2_pin,50)
            pwm_1.start(8)
            pwm_2.start(8)
            pwm_1.ChangeDutyCycle(8)
            pwm_2.ChangeDutyCycle(8)
            time.sleep(0.2)
            pwm_1.stop()
            pwm_2.stop()
            
        print (condition)

        emit('server_light',{'light':condition})

        humidity,temperature = Adafruit_DHT.read(sensor,temp_sensor_pin)        
        if humidity is not None and temperature is not None:
            temp = 'Temp={0:0.1f}*C  '.format(temperature)
            
            if (temperature > 25):
                temp = temp + 'hot,turning on air conditioner'
                GPIO.output(air_con_1_pin,GPIO.LOW)
                GPIO.output(air_con_2_pin,GPIO.LOW)
            else:
                temp = temp + 'cool! turning off air conditioner'
                GPIO.output(air_con_1_pin,GPIO.HIGH)
                GPIO.output(air_con_2_pin,GPIO.HIGH)

        else:
            temp = 'Geting Temperature data'
       
        emit('server_temp',{'temp':temp})

    elif (request == led_on):
        GPIO.output(led_pin,GPIO.HIGH)

    elif (request == led_off):
        GPIO.output(led_pin,GPIO.LOW)
      
    elif (request == air_con_1_on):
        GPIO.output(air_con_1_pin,GPIO.LOW)

    elif (request == air_con_1_off):
        GPIO.output(air_con_1_pin,GPIO.HIGH)

    elif (request == air_con_2_on):
        GPIO.output(air_con_2_pin,GPIO.LOW)

    elif (request == air_con_2_off):
        GPIO.output(air_con_2_pin,GPIO.HIGH)

    elif (request == curtain_1_on):
        pwm_1 = GPIO.PWM(curtain_1_pin,50)
        pwm_1.start(8)
        pwm_1.ChangeDutyCycle(8)
        time.sleep(0.2)
        pwm1.stop()
        
    elif (request == curtain_1_off):
        
        pwm_1 = GPIO.PWM(curtain_1_pin,50)
        pwm_1.start(3)
        pwm_1.ChangeDutyCycle(3)
        time.sleep(0.2)
        pwm1.stop()
    elif (request == curtain_2_on):
        pwm_2 = GPIO.PWM(curtain_2_pin,50)
        pwm_2.start(8)
        pwm_2.ChangeDutyCycle(8)
        time.sleep(0.2)
        pwm2.stop()
    elif (request == curtain_2_off):
        
        pwm_2 = GPIO.PWM(curtain_2_pin,50)
        pwm_2.start(3)
        pwm_2.ChangeDutyCycle(3)
        time.sleep(0.2)
        pwm2.stop()
    elif (request == light_sensor_read):
        light_env = GPIO.input(light_sensor_pin)
        if (light_env == 0):
            condition = 'bright'
        else :
            condition = 'dim'

        print (condition)

        emit('server_light',{'light':condition})

    elif (request == temp_sensor_read):

        
        humidity,temperature = Adafruit_DHT.read(sensor,temp_sensor_pin)        
        
        if humidity is not None and temperature is not None:
            temp = '{0:0.1f}*C'.format(temperature)
        else:
            temp = 'Getting temperature data'
       
        print(temp)
        emit('server_temp',{'temp':temp})
        
    elif (request == camera_take_photo):
        now = datetime.datetime.now()
        camera = picamera.PiCamera()
        strnow = str(now)
        savepath = '/home/pi/Desktop/YPEC/static/img/'+strnow+'image.jpg'
        camera.hflip = True
        camera.vflip = True
        camera.capture(savepath)
        camera.close()

        emit('server_camera',{'camera':str(now)})
    else:
        print ("unexpected value input")
if __name__ == "__main__": 
    app.debug = True
    socketio.run(app,host='0.0.0.0', port=85)
