#1st function named main.py
import cv2
import mediapipe as mp
import numpy as np
import time
import serial
from time import sleep
import main2

#def buzz(a):
  #import serial
  #arduinoData=serial.Serial('com8 ' , 115200)
  #while(True):
   #sleep(2)
   #Amd=input ( 'Please Enter Your Command:') 
   #if a==1:
     #t="ON"
   #else:
    # t="OFF"   
   #cmd=t +'\r'
   #arduinoData.write(cmd. encode( ))
   #break
    
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=.5, min_tracking_confidence=.5)

mp_drawing = mp.solutions.drawing_utils

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)


cap=cv2.VideoCapture(0)
DEL=0
r=0
k=0
m=0

while cap.isOpened():
    success, image = cap.read()

    start = time.time()
    # Flip the image horizontally for a later selfie-view display
    # Also convert the color space from BGR to RGB
    image= cv2.cvtColor(cv2.flip(image,1),cv2.COLOR_BGR2RGB)
    #To improve performance
    image.flags.writeable = False
    #Get the result
    results=face_mesh.process(image)
    #To improve performace
    image.flags.writeable=True
    #Convert the color space from RGB to BGR
    image=cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    
    img_h,img_w,img_c= image.shape
    face_3d=[]
    face_2d=[]
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            for idx,lm in enumerate(face_landmarks.landmark):
                if idx==33 or idx==263 or idx==1 or idx==61 or idx ==291 or idx==199:
                    if idx==1:
                        nose_2d=(lm.x * img_w,lm.y * img_h)
                        nose_3d=(lm.x * img_w,lm.y * img_h,lm.z * 3000)
                    x,y=int(lm.x * img_w), int(lm.y * img_h)
                    #Get the 2D coordinates
                    face_2d.append([x,y])
                    #Get the 3D Coordinates
                    face_3d.append([x,y,lm.z])
            #Convert it to the NumPy array
            face_2d=np.array(face_2d,dtype=np.float64)
            #Convert it to the NumPy array
            face_3d=np.array(face_3d,dtype=np.float64)
            #The camera matrix
            focal_length=1* img_w
            cam_matrix=np.array([ [ focal_length,0,img_h/2],
                                  [0,focal_length,img_w/2], 
                                  [0,0,1]])

            #The distortion parameters
            dist_matrix=np.zeros((4,1),dtype=np.float64)
            #Solve PnP
            success,rot_vec,trans_vec=cv2.solvePnP(face_3d,face_2d,cam_matrix, dist_matrix)
            #Get rotational matrix
            rmat,jac=cv2.Rodrigues(rot_vec)
            #Get angles
            angles,mtxR,mtxQ,Qx,Qy,Qz=cv2.RQDecomp3x3(rmat)
            #Get the y rotation degree
            x=angles[0]*360
            y=angles[1]*360
            z=angles[2]*360
            #See where the head's tilting
            p=0
            if y<-14.5:
                text="Looking Left"
            elif y>14.5:
                text="Looking Right"
            elif x<-8:
                text="Looking Down"
            elif x>13:
                text="Looking Up"
            else:
                p=1
                text="Forward"
            #Display the nose direction
            nose_3d_projection,jacobian=cv2.projectPoints(nose_3d,rot_vec,trans_vec,cam_matrix,dist_matrix)
            p1=(int(nose_2d[0]),int(nose_2d[1]))
            p2=(int(nose_2d[0]+y*10),int(nose_2d[1]-x*10))

            cv2.line(image,p1,p2,(255,0,0),3)

            #Add text on the image
            cv2.putText(image,text,(20,50),cv2.FONT_HERSHEY_SIMPLEX,2,(0,255,0),2)
            cv2.putText(image,"x:"+str(np.round(x,2)),(500,50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),4)  
            cv2.putText(image,"y:"+str(np.round(y,2)),(500,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),4)
        cv2.putText(image,"z:"+str(np.round(z,2)),(500,150),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),4)
        cv2.waitKey(5)
        end=time.time()
        totalTime=end-start
        if p==0:
            DEL=DEL+totalTime
        else:
            DEL=0
        #print("DEL:",DEL)    
        #5sec in real=2 time here
        print("DEL value:",DEL)
        if DEL>1 and DEL<1:
           print("BUZZER")
           k=1

           #arduinoData=serial.Serial('com8 ' , 115200)
           #cmd=input ( 'Please Enter Your Command:') 
           #cmd="ON"+'\r'
           #arduinoData.write(cmd. encode( ))
           main2.buzz("ON")
        elif DEL>1.5:
           print("Mayday")
           main2.mayday("ON")
        elif k:
           r=0
           k=0
           m=0
           main2.phew("OFF") 


        if totalTime!=0:
             fps=1/totalTime
        else:
             fps=1000

        #print("FPS:",fps)
    
        cv2.putText(image,f'FPS:{int(fps)}',(20,450),cv2.FONT_HERSHEY_SIMPLEX,1.5,(0,255,0),2)
        mp_drawing.draw_landmarks(
                    image=image,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=drawing_spec,
                    connection_drawing_spec=drawing_spec)

    cv2.imshow('Head Pose Estimation',image)
    if cv2.waitKey(5) & 0xFF==ord('c'):
        break
    #cv2.waitKey(300)

cap.release() 


 
