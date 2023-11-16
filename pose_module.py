import cv2, time, math
import mediapipe as mp
import time
import math

class poseDetector():
 
    def __init__(self, mode=False, upBody=False, smooth=True,
                 detectionCon=0.5, trackCon=0.5):
 
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon
 
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose

        self.pose = self.mpPose.Pose(self.mode, min_detection_confidence=detectionCon, min_tracking_confidence=trackCon)
 
    def findPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks and draw:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                if id not in [1,2,3,4,5,6,7,8,9,10,17,18,19,20,]:  # Skip facial landmarks and fingers
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

            # Manually draw connections, avoiding facial landmarks
            for conn in self.mpPose.POSE_CONNECTIONS:
                if conn[0] > 10 and conn[1] > 10:  # Exclude connections involving facial landmarks
                    pt1 = self.results.pose_landmarks.landmark[conn[0]]
                    pt2 = self.results.pose_landmarks.landmark[conn[1]]
                    x1, y1 = int(pt1.x * w), int(pt1.y * h)
                    x2, y2 = int(pt2.x * w), int(pt2.y * h)
                    cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
        return img

 
    def findPosition(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList