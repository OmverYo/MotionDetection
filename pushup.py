import cv2
import mediapipe as mp
import time

mp_drawing = mp.solutions.drawing_utils
drawSpecific = mp.solutions.pose
mp_pose = mp.solutions.pose

def distanceCalculate(p1, p2):
    """p1 and p2 in format (x1, y1) and (x2, y2) tuples"""
    dis = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
    
    return dis

pushUpStart = 0
pushUpCount = 0

# For webcam input:
cap = cv2.VideoCapture(0)

with mp_pose.Pose(min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:

    while cap.isOpened():
        success, image = cap.read()

        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue
        
        try:
            results = pose.process(image)
            image_height, image_width, _ = image.shape

            nosePoint = (int(results.pose_landmarks.landmark[0].x*image_width), int(results.pose_landmarks.landmark[0].y*image_height))
            leftWrist = (int(results.pose_landmarks.landmark[15].x*image_width), int(results.pose_landmarks.landmark[15].y*image_height))
            rightWrist = (int(results.pose_landmarks.landmark[16].x*image_width), int(results.pose_landmarks.landmark[16].y*image_height))
            leftShoulder = (int(results.pose_landmarks.landmark[11].x*image_width), int(results.pose_landmarks.landmark[11].y*image_height))
            rightShoulder = (int(results.pose_landmarks.landmark[12].x*image_width), int(results.pose_landmarks.landmark[12].y*image_height))

            if distanceCalculate(rightShoulder, rightWrist) < 130:
                pushUpStart = 1
            
            elif pushUpStart and distanceCalculate(rightShoulder, rightWrist) > 250:
                pushUpCount = pushUpCount + 1
                pushUpStart = 0

            print(pushUpCount)

        except:
            success, image = cap.read()

        # Flip the image horizontally for a selfie-view display.
        cv2.imshow('MediaPipe Pose', image)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()