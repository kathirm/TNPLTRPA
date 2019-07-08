import cv2
import numpy as np
face_cascade = cv2.CascadeClassifier('/tmp/haarcascade_frontalface_default.xml') 
eye_cascade = cv2.CascadeClassifier('/tmp/haarcascade_eye.xml') 
img = cv2.imread('/tmp/sachin.jpg') 
while 1:
    
    #ret, img = cap.read() 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=2) 
    for (x,y,w,h) in faces: 

        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2) 
        roi_gray = gray[y:y+h, x:x+w] 
        roi_color = img[y:y+h, x:x+w] 
        eyes = eye_cascade.detectMultiScale(roi_gray) 
        print eyes
        for (ex,ey,ew,eh) in eyes: 
            
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,127,255),2) 
    cv2.imshow('img',img) 
    k = cv2.waitKey(30) & 0xff
    if k == 27: 
        break
cap.release() 
cv2.destroyAllWindows()
