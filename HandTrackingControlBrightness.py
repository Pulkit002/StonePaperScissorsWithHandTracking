# Importing Libraries
import cv2
import mediapipe as mp
from math import hypot
import screen_brightness_control as sbc
import numpy as np
# Initializing the Model
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75,
    max_num_hands=2)
 
Draw = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# Start capturing video from webcam
cap = cv2.VideoCapture(0)

def make_480p():
    cap.set(3, 640)
    cap.set(4, 480)

def change_res(width, height):
    cap.set(3, width)
    cap.set(4, height)

make_480p()
change_res(1280, 720)
 
while True:
    # Read video frame by frame
    _,frame = cap.read()
     
    #Flip image
    frame=cv2.flip(frame,1)
     
    # Convert BGR image to RGB image
    frameRGB = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
     
    # Process the RGB image
    Process = hands.process(frameRGB)
     
    landmarkList = []
    # if hands are present in image(frame)
    if Process.multi_hand_landmarks:
        # detect handmarks
        for handlm in Process.multi_hand_landmarks:
            for _id,landmarks in enumerate(handlm.landmark):
                # store height and width of image
                height,width,color_channels = frame.shape
                 
                # calculate and append x, y coordinates
                # of handmarks from image(frame) to lmList
                x,y = int(landmarks.x*width),int(landmarks.y*height)             
                landmarkList.append([_id,x,y])
             
            # draw Landmarks
            Draw.draw_landmarks(frame,handlm,mpHands.HAND_CONNECTIONS,mp_drawing_styles.get_default_hand_landmarks_style(),
                                           mp_drawing_styles.get_default_hand_connections_style())
     
    # If landmarks list is not empty
    if landmarkList != []:
        # store x,y coordinates of (tip of) thumb 
        x_1,y_1 = landmarkList[4][1],landmarkList[4][2]
         
        # store x,y coordinates of (tip of) index finger
        x_2,y_2 = landmarkList[8][1],landmarkList[8][2]
         
        # draw circle on thumb and index finger tip
        cv2.circle(frame,(x_1,y_1),7,(0,255,0),cv2.FILLED)
        cv2.circle(frame,(x_2,y_2),7,(0,255,0),cv2.FILLED)
         
        # draw line from tip of thumb to tip of index finger
        cv2.line(frame,(x_1,y_1),(x_2,y_2),(0,255,0),3)
         
        # calculate square root of the sum
        # of squares of the specified arguments.
        L = hypot(x_2-x_1,y_2-y_1)
         
        # 1-D linear interpolant to a function
        # with given discrete data points
        # (Hand range 15 - 220, Brightness range 0 - 100),
        # evaluated at length.
        b_level = np.interp(L,[15,220],[0,100])
     
        # set brightness
        sbc.set_brightness(int(b_level))
 
    # Display Video and when 'q' is entered, destroy the window
    
    cv2.putText(frame, "Press g to play Stone-Paper-Scissors game" ,(20,660),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,0),1)
    cv2.putText(frame, "Press v to adjust volume" ,(20,675),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,0),1)
    cv2.putText(frame, "Press q to go to handsign recognition window" ,(20,690),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,0),1)
    cv2.putText(frame, "Press esc to quit" ,(20,705),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,0),1) 
    
    cv2.imshow('Image', frame)
    key=cv2.waitKey(1) & 0xFF
    if key == ord('q'): 
        import HandTrackingMin
    elif key == ord('v'):
        import HandTrackingControlVolume
    elif key == ord('g'):
        import StonePaperScissors
    elif key == 27:
        break