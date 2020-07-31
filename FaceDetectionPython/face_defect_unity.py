import numpy as np
import cv2
import math
import socket
import time

UDP_IP = "127.0.0.1"
UDP_PORT = 5065

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

last = "none"


# Open Camera
try:
    default = 0 # Try Changing it to 1 if webcam not found
    cap = cv2.VideoCapture(default)
    cascade_classifier = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
except:
    print("No Camera Source Found!")


    
while True:
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, 0)
    detections = cascade_classifier.detectMultiScale(frame,1.3,5)
    
    if (len(detections) > 0):
        x,y,w,h = detections[0]
        print(detections)
        print(ret)
        a = int(x+(w/2))
        b = int(y+(h/2))
        break
    else:
        print("wait")
    cv2.imshow('frame',frame)    
    key = cv2.waitKey(1)    
while True:
    ret, frame = cap.read()
    frame = cv2.cvtColor(frame, 0)
    detections = cascade_classifier.detectMultiScale(frame,1.3,5)
    frame = cv2.circle(frame, (a, b), 20, (0, 0, 255), 1)
    frame = cv2.circle(frame, (a, b), 50, (0, 0, 255), 1)
    frame = cv2.circle(frame, (a, b), 1, (0, 255, 0), 3)
    
    if (len(detections) > 0):
        (x,y,w,h) = detections[0]
    a1,b1 = int(x+(w/2)),int(y+(h/2))
    x_dis = a-a1
    y_dis = b-b1
    frame = cv2.circle(frame, (a1, b1), 1, (0, 255, 0), 3)
    if abs(x_dis)>abs(y_dis) and abs(x_dis)>50:
        if x_dis<0:
            print('Left')
            if last != "Left":
                sock.sendto( ("Left!").encode(), (UDP_IP, UDP_PORT) )
                last = "Left"
        else:
            print('Right')
            if last != "Right":
                sock.sendto( ("Right!").encode(), (UDP_IP, UDP_PORT) )
                last = "Right"
    elif abs(x_dis)<abs(y_dis) and abs(y_dis)>20:
        if y_dis<0:
            print("down")
        else:
            print("up")
            if (last != "Up"):
                sock.sendto( ("JUMP!").encode(), (UDP_IP, UDP_PORT) )
                last = "Up"
    else:
        last = "None"            
    cv2.imshow('frame',frame)

    print("last is ", last)    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()