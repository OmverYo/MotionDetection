import cv2
import mediapipe as mp
import numpy as np
import json

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture("BX_Dance01_Full_FV_A113C176.mp4")

fps = round(cap.get(cv2.CAP_PROP_FPS), 0)
total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
timestamps = [cap.get(cv2.CAP_PROP_POS_MSEC)]

lmList = []

with mp_pose.Pose(model_complexity = 1, min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()

        if not success:
            print("Ignoring empty camera frame.")
            break

        results = pose.process(image)

        timestamps = [int(cap.get(cv2.CAP_PROP_POS_MSEC))]

        if timestamps[-1] % 1001 == 0:
            print(timestamps)
            for id, lm in enumerate(results.pose_landmarks.landmark):
                if id not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                    h, w, c = image.shape
                    # print(id, lm.x, lm.y)
                    # print(id, lm)
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append((id, cx, cy))

        if cv2.waitKey(5) & 0xFF == 27:
            break

with open('data.json', 'w') as f:

    json.dump(lmList, f)

cap.release()

cv2.destroyAllWindows()