# lpsmc-isac

# The Ideal School Automation Control (ISAC) 
# Young Professionals Exhibition & Competition 2016 Championship in secondary school section
# paroskwan@gmail.com

# The Ideal School Automation Control (ISAC) was developed when I was working in a local secondary school known as 
# Liu Po Shan Memorial College (LPSMC), together with students we developed this prototype to automate the classroom 
# with the aid of Raspberry Pi. This project get the Championship in secondary school section in YPEC 2016 HK section.

# The code uploaded are NOT COMPLETE, just the main code are uploaded, files like css/js lib are omitted, so it is not possible to "download and run " the code directly 

# DETAIL EXPLANATION 
#The raspberry pi is acting as a server,with flask-socket.io running . To control ISAC, the client, usually a computer or a phone, has to be connect to the #same local area network with the RPi. We can either use a phone/computer to enter the control panel page.
#In a manual mode, when a button is clicked on the client’s side, a JSON object that represent the action is sent to the RPi #server via WebSocket. Upon receiving the message, the RPi will alter the output of that particular GPIO to start/shut down #on electrical appliance. Furthermore, the client will repeatedly send a message to the server to ask for the latest light #and temperature data. After the client reveives the messages emitted for the server, the client will update the sensor data #by JavaScript.
#In an automatic mode, the client will repeatedly send a message to the server to ask for automation, i.e. control of the # output of GPIO by the sensor’s  data. Those sensor’s data are also sent to the client for Display also.


