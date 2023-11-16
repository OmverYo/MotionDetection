import cv2
import mediapipe as mp
import numpy as np
import json

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

frame_counter = 0

cap = cv2.VideoCapture("BX_Dance01_01_FV_A113C177.mp4")

fps = cap.get(cv2.CAP_PROP_FPS)
total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)

lmList = []

with mp_pose.Pose(model_complexity = 1, min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()

        if not success:
            print("Ignoring empty camera frame.")
            break

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (640, 480))
        results = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        frame_counter += 1

        if (round(frame_counter / fps, 1) == 0.5 or round(frame_counter / fps, 1) == 0):
            for id, lm in enumerate(results.pose_landmarks.landmark):
                if id not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                    h, w, c = image.shape
                    # print(id, lm.x, lm.y)
                    # print(id, lm)
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    lmList.append([id, cx, cy])
            
            frame_counter = 0

        cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))

        if cv2.waitKey(5) & 0xFF == 27:
            break

# np.save("C:/Users/pc1/Desktop/CameraPractice/x_save", lmList)
# x_save_load = np.load("C:/Users/pc1/Desktop/CameraPractice/x_save.npy")
# result = list(x_save_load)
# print(result)

with open('data.json', 'w') as f:

    json.dump(lmList, f)

cap.release()

cv2.destroyAllWindows()