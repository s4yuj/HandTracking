import cv2
import time 
import numpy as np
import tracking as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

wCam, hCam = 640, 480

ptime = 0
ctime = 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)


detector = htm.handDetector(detectionCon=0.7)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)

volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0
# print(volRange)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = detector.findHands(frame)

    lmList=detector.findPosition(frame, draw=False)
    if len(lmList)!=0:
        # print(lmList[4],lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx , cy = (x1+x2)//2, (y1+y2)//2
    
        
        cv2.circle(frame, (x1, y1), 10, (255, 255, 0), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 10, (255, 255, 0), cv2.FILLED)
        cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 0), 3)
        cv2.circle(frame, (cx, cy), 10, (0, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        vol = np.interp(length, [50, 300], [minVol, maxVol])
        volBar = np.interp(length, [50, 300], [400, 150])
        volPer = np.interp(length, [50, 300], [0, 100])

        volume.SetMasterVolumeLevel(vol, None)

        if length<50:
            cv2.circle(frame, (cx, cy), 10, (0, 255, ), cv2.FILLED)

    cv2.rectangle(frame, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(frame, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
    cv2.putText(frame, f'{int(volPer)}%', (40, 450), cv2.FONT_HERSHEY_DUPLEX,1 , (0, 250, 0, 3))

    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime = ctime
    cv2.putText(frame, f'fps {str(int(fps))}' , (10, 30), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 255), 3)

    cv2.imshow("webcam", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
