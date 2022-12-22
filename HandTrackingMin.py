import cv2
import mediapipe as mp
import vlc
p=vlc.MediaPlayer("spiderman.mp3")

def getHandMove(hand_landmarks):
    landmarks = hand_landmarks.landmark
    if landmarks[4].y < landmarks[3].y and landmarks[3].y < landmarks[2].y and landmarks[2].y<landmarks[1].y and landmarks[5].y<landmarks[9].y and landmarks[9].y<landmarks[13].y and landmarks[13].y<landmarks[17].y and landmarks[4].y<landmarks[5].y and landmarks[4].y<landmarks[9].y and landmarks[4].y<landmarks[13].y and landmarks[4].y<landmarks[17].y:
        return "Thumbs up"
    elif landmarks[8].y < landmarks[7].y and landmarks[7].y<landmarks[6].y and landmarks[6].y<landmarks[5].y and landmarks[12].y > landmarks[9].y and landmarks[16].y > landmarks[13].y and landmarks[20].y > landmarks[17].y and landmarks[20].y > landmarks[4].y:
        return "One"
    elif round(landmarks[8].x,1)==round(landmarks[4].x,1) and landmarks[4].y > landmarks[8].y and landmarks[0].y>landmarks[4].y:
        return "small"
    elif landmarks[4].y > landmarks[3].y and landmarks[3].y > landmarks[2].y and landmarks[2].y>landmarks[1].y and landmarks[5].y>landmarks[9].y and landmarks[9].y>landmarks[13].y and landmarks[13].y>landmarks[17].y :
        return "Thumbs down"
    elif landmarks[8].y<landmarks[5].y and landmarks[20].y<landmarks[17].y and landmarks[9].y<landmarks[12].y and landmarks[13].y<landmarks[16].y :
        return "Rock!"
    elif landmarks[8].y>landmarks[5].y and landmarks[20].y>landmarks[17].y and landmarks[9].y>landmarks[12].y and landmarks[13].y>landmarks[16].y :
        return "Spidey Time"
        

cap = cv2.VideoCapture(0)  # to run the webcam

def make_480p():
    cap.set(3, 640)
    cap.set(4, 480)

def change_res(width, height):
    cap.set(3, width)
    cap.set(4, height)

make_480p()
change_res(1280, 720)

Text=""

mpHands = mp.solutions.hands  # formality
mp_drawing_styles = mp.solutions.drawing_styles
hands = mpHands.Hands()  # this will sometimes detect and sometimes track depending upon the confidence level
mpDraw = mp.solutions.drawing_utils  # this will draw the lines between the points


while True:
    success, img = cap.read()  # to run the webcam
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)  # This prints the coordinates of hand. If no hand is detected it returns the value none
    # results.multi_hand_landmarks will be interpreted as true if a hand is detected otherwise false. Hence, we can use if else conditions using this
    
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            for id, lm in enumerate(handLms.landmark):
                # print(id,lm) # this will print id (i.e. index from 0 t0 20 as there are total 21 landmarks on each hand) and the coordinates of those landmarks
                h, w, c = img.shape  # height, width, channels of our image
                cx, cy = int(lm.x * w), int(lm.y * h)  # cx and cy are the coordinates of landmarks in pixels
                # print(id, cx, cy)
                # if id ==0:
                cv2.circle(img, (cx, cy), 7, (255, 255, 255), cv2.FILLED)
    
            mpDraw.draw_landmarks(img, handLms,
                                  mpHands.HAND_CONNECTIONS,
                                  mp_drawing_styles.get_default_hand_landmarks_style(),
                                  mp_drawing_styles.get_default_hand_connections_style())  # if we remove mpHands.Hand_CONNECTIONS, then we will just get the points. no lines between them
    hls=results.multi_hand_landmarks
    if hls!=None:
        if len(hls)==1:
            handsign=getHandMove(hls[0])
            if handsign=="Spidey Time":
                p.play()
                Text=f"{handsign}"
            else:
                p.stop()
                Text=f"{handsign}" 
        elif len(hls)==2:
            handsign="Please use one hand"
            Text=f"{handsign}"   
    else:
        handsign="No Handsign"
        Text=f"{handsign}"
    
    cv2.rectangle(img,(20,20),(1260,65), (0,0,0),2)
    if Text=="Please use one hand" or Text=="No Handsign":
        cv2.putText(img,str(Text),(50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (68, 58, 201),2)
        # (where to put the text, what to put(string in our case), position, font, scale, color, thickness)
    else:
        cv2.putText(img,str(Text),(50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (163, 75, 91),2) 
    cv2.putText(img, "Press b to adjust brightness" ,(20,660),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,0),1)
    cv2.putText(img, "Press v to adjust volume" ,(20,675),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,0),1)
    cv2.putText(img, "Press g to play Stone-Paper-Scissors" ,(20,690),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,0),1)
    cv2.putText(img, "Press esc or q to quit" ,(20,705),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,0),1)

    cv2.imshow("Image", img)  # to run the webcam
    #cv2.waitKey(1)  # to run the webcam
    key=cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27: #27-->esc key
        break
    elif key == ord('b'):
        import HandTrackingControlBrightness
    elif key == ord('g'):
        import StonePaperScissors
    elif key== ord('v'):
        import HandTrackingControlVolume