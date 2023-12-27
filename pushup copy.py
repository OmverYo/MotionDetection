import cv2
import mediapipe as mp
import time
import random

mp_drawing = mp.solutions.drawing_utils
drawSpecific = mp.solutions.pose
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5)

def distanceCalculate(p1, p2):
    """p1 and p2 in format (x1, y1) and (x2, y2) tuples"""
    dis = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
    
    return dis

randomCounter = random.randint(2, 5)

Start = 0
Count = 0

cap = cv2.VideoCapture(0)

startTimer = time.time()
endTimer = time.time()

while cap.isOpened():
    success, image = cap.read()

    if not success:
        print("Ignoring empty camera frame.")

        continue
    
    try:
        results = pose.process(image)
        image_height, image_width, _ = image.shape

        leftAnkle = (int(results.pose_landmarks.landmark[27].x*image_width), int(results.pose_landmarks.landmark[27].y*image_height))
        rightAnkle = (int(results.pose_landmarks.landmark[28].x*image_width), int(results.pose_landmarks.landmark[28].y*image_height))

        if int(endTimer) - int(startTimer) == randomCounter:
            print("GO")
            print("GO")
            print("GO")
            print("GO")
            print("GO")
            print("GO")
            print("GO")
            print("GO")
            print("GO")
            print("GO")
            print("GO")
            print("GO")
            print("GO")
            print("GO")
            print("GO")
            print("GO")
            print("GO")

            startTimer = time.time()

        if distanceCalculate(leftAnkle, rightAnkle) < 50:
            Start = 1
            endTimer = time.time()

        elif Start and distanceCalculate(leftAnkle, rightAnkle) > 60:
            endTimer = time.time()
            
            Count = Count + 1
            Start = 0

            print("Time Taken:", round((endTimer - startTimer), 3))

            randomCounter = random.randint(2, 5)

            print("Random:", randomCounter)
            print("Count:", Count)

            startTimer = time.time()

    except:
        success, image = cap.read()

    cv2.imshow('MediaPipe Pose', image)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()