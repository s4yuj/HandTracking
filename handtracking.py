import cv2
import mediapipe as mp
import time

cap= cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()

mpDraw= mp.solutions.drawing_utils



while True:
    ret, frame = cap.read()
    frame=cv2.flip(frame,1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    results = hands.process(frame_rgb)
    if (results.multi_hand_landmarks):
        
        for landMark in results.multi_hand_landmarks:

            for id, lm in enumerate(landMark.landmark):
                (h,w,c) = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)

                # print(id, cx, cy )
                # if id == 0:
                #     cv2.circle(frame, (cx, cy), 25, (255, 0, 255), cv2.FILLED)
            mpDraw.draw_landmarks(frame, landMark, mpHands.HAND_CONNECTIONS)

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    
    cv2.putText(frame, str(int(fps)) , (10, 70), cv2.FONT_HERSHEY_DUPLEX, 3, (255, 0, 255), 3)


    cv2.imshow("webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
