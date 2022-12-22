import cv2
import mediapipe as mp
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import numpy as np

cap = cv2.VideoCapture(0)

def make_480p():
    cap.set(3, 640)
    cap.set(4, 480)

def change_res(width, height):
    cap.set(3, width)
    cap.set(4, height)

make_480p()
change_res(1280, 720)
 
mpHands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# Accessing the system speaker using pycaw library
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

volbar=400
volper=0

volMin, volMax = volume.GetVolumeRange()[:2]
while True:
    success, img = cap.read() #If camera works capture an image
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    
    lmList = []
    if results.multi_hand_landmarks:
        for handlandmark in results.multi_hand_landmarks:
             for id, lm in enumerate(handlandmark.landmark):
                  # Get Finger Joint Points
                  h, w, c = img.shape
                  cx, cy = int(lm.x * w), int(lm.y * h)
                  lmList.append([id, cx, cy]) 
             mpDraw.draw_landmarks(img, handlandmark, mpHands.HAND_CONNECTIONS,mp_drawing_styles.get_default_hand_landmarks_style(),
                                           mp_drawing_styles.get_default_hand_connections_style()) 
        if lmList != []:
            # getting the value at a point
                             #x            #y
            x1, y1 = lmList[4][1], lmList[4][2]  # tip of thumb
            x2, y2 = lmList[8][1], lmList[8][2]  # tip of index finger
            
            #creating circle at the tips of thumb and index finger
            cv2.circle(img, (x1, y1), 15, (255, 0, 0), cv2.FILLED)  #image #fingers #radius #rgb
            cv2.circle(img, (x2, y2), 15, (255, 0, 0), cv2.FILLED)  #image #fingers #radius #rgb
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3) # creates a line between tips of index finger and thumb
            
            # Distance b/w tips using hypotenuse function from numpy library
            length = hypot(x2 - x1, y2 - y1)
            vol = np.interp(length, [30, 350], [volMin, volMax])
            volper=np.interp(length,[30,150],[0,100])

            volume.SetMasterVolumeLevel(vol, None)
            
            cv2.putText(img,f"Volume Percent: {int(volper)}%",(10,40),cv2.FONT_ITALIC,1,(0,0,0),3)
            
    cv2.putText(img, "Press b to adjust brightness" ,(20,660),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,0),1)
    cv2.putText(img, "Press v to adjust volume" ,(20,675),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,0),1)
    cv2.putText(img, "Press q to go to handsign recognition window" ,(20,690),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,0),1)
    cv2.putText(img, "Press esc to quit" ,(20,705),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,0),1)        
    
    cv2.imshow('Image', img) 
    
    key=cv2.waitKey(1) & 0xFF
    if key == ord('q'): 
        import HandTrackingMin
    elif key == ord('b'):
        import HandTrackingControlBrightness
    elif key == ord('g'):
        import StonePaperScissors
    elif key == 27:
        break