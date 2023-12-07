import os
import cv2
import mediapipe as mp
import json

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(model_complexity = 0, min_detection_confidence = 0.5, min_tracking_confidence = 0.5)

cwd = os.getcwd().replace("\\", "/") + "/"

onlyfiles = [f for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f))]

onlyfiles.remove("print.py")

for x in onlyfiles:
    cap = cv2.VideoCapture(cwd + x)

    fps = round(cap.get(cv2.CAP_PROP_FPS), 0)
    total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    timestamps = [cap.get(cv2.CAP_PROP_POS_MSEC)]

    lmList = []

    while cap.isOpened():
        success, image = cap.read()

        results = pose.process(image)

        timestamps = [int(cap.get(cv2.CAP_PROP_POS_MSEC))]

        if timestamps[-1] % 1001 == 0:
            print(fps, total_frames, timestamps)
            for id, lm in enumerate(results.pose_landmarks.landmark):
                if id not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                    h, w, c = image.shape
                    # print(id, lm.x, lm.y)
                    # print(id, lm)
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append((id, cx, cy))

    with open(x + ".json", 'w') as f:
        json.dump(lmList, f)

    cap.release()
    cv2.destroyAllWindows()