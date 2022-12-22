import cv2 as cv
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def getHandMove(hand_landmarks):
    landmarks = hand_landmarks.landmark
    if all([landmarks[i].y < landmarks[i+3].y for i in range(9,20,4)]): 
        return "Rock"
    elif landmarks[0].y >landmarks[2].y and landmarks[0].y >landmarks[4].y and landmarks[0].y >landmarks[5].y and landmarks[5].y >landmarks[8].y and landmarks[0].y >landmarks[9].y and landmarks[9].y >landmarks[12].y and landmarks[0].y >landmarks[13].y and landmarks[13].y >landmarks[16].y and landmarks[0].y >landmarks[17].y and landmarks[17].y >landmarks[20].y:
        return "Paper"
    else:
        return "Scissor"
vid = cv.VideoCapture(0)

def make_480p():
    vid.set(3, 640)
    vid.set(4, 480)

def change_res(width, height):
    vid.set(3, width)
    vid.set(4, height)

make_480p()
change_res(1280, 720)

clock = 0
pi_move = p2_move = None
gameText = ""
success = True

with mp_hands.Hands(model_complexity=0,
                     min_detection_confidence=0.5,
                     min_tracking_confidence=0.5) as hands:
     while True:
         ret, frame = vid.read()
         if not ret or frame is None: break
         frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
         
         results = hands.process(frame)
         
         frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
         if results.multi_hand_landmarks:
             for hand_landmarks in results.multi_hand_landmarks:
                 mp_drawing.draw_landmarks(frame,
                                           hand_landmarks,
                                           mp_hands.HAND_CONNECTIONS,
                                           mp_drawing_styles.get_default_hand_landmarks_style(),
                                           mp_drawing_styles.get_default_hand_connections_style())
                 
         frame = cv.flip(frame, 1)
         
         if 0 <= clock < 40:
             success = True
             gameText="Ready?"
         elif clock < 60:
             gameText="3..."
         elif clock < 80:
             gameText="2..."
         elif clock < 100:
             gameText="1..."
         elif clock < 120:
             gameText="Go!"
         elif clock==120:
             hls=results.multi_hand_landmarks
             if hls and len(hls)==2:
                 p1_move=getHandMove(hls[0])
                 p2_move=getHandMove(hls[1])
             else:
                 success = False
         elif clock < 200:
             if success:
                 gameText= f"Player 1: {p1_move} | Player 2: {p2_move}"
                 if p1_move==p2_move:
                     gameText=f"{gameText}| Game is tied."
                 elif p1_move=="Paper" and p2_move=="Rock":
                     gameText=f"{gameText}| Player 1 Wins."
                 elif p1_move=="Rock" and p2_move=="Scissor":
                     gameText=f"{gameText}| Player 1 Wins."
                 elif p1_move=="Scissor" and p2_move=="Paper":
                     gameText=f"{gameText}| Player 1 Wins."
                 else:
                     gameText=f"{gameText}| Player 2 Wins."
             else:
                 gameText="Didn't play properly!"  
         
         cv.rectangle(frame,(20,20),(1260,110), (0,0,0),2)
         cv.putText(frame, f"Clock: {clock}",(50,50),cv.FONT_HERSHEY_SIMPLEX, 1,(0,0,0),2) 
         cv.putText(frame, gameText ,(50,95),cv.FONT_HERSHEY_SIMPLEX, 1,(250, 189, 115),2)
         cv.putText(frame, "Press b to adjust brightness" ,(20,660),cv.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,0),1)
         cv.putText(frame, "Press v to adjust volume" ,(20,675),cv.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,0),1)
         cv.putText(frame, "Press q to go to handsign recognition window" ,(20,690),cv.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,0),1)
         cv.putText(frame, "Press esc to quit" ,(20,705),cv.FONT_HERSHEY_SIMPLEX, 0.5,(0,0,0),1)
         clock = (clock+1) % 200
             
         cv.imshow("Image",frame)
         
         key=cv.waitKey(1) & 0xFF
         if key == ord('q'): 
            import HandTrackingMin
         elif key == ord('b'):
            import HandTrackingControlBrightness
         elif key == ord('v'):
            import HandTrackingControlVolume
         elif key == 27:
            break
vid.release()
cv.destroyAllWindows()