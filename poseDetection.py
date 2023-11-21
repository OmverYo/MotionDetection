import cv2
import mediapipe as mp
import numpy as np
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_selfie_segmentation = mp.solutions.selfie_segmentation
mp_pose = mp.solutions.pose

# 배경화면의 색상을 지정합니다
BG_COLOR = (0, 255, 0) # GREEN

frame_counter = 0

cap = cv2.VideoCapture(0)

with mp_selfie_segmentation.SelfieSegmentation(model_selection = 1) as selfie_segmentation, mp_pose.Pose(model_complexity = 0, min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:
    # 배경화면의 이미지를 설정 할 수 있으나 없음으로 설정
    bg_image = None

    start = round(time.time(), 1)
    
    while cap.isOpened():
        success, image = cap.read()

        if not success:
            print("Ignoring empty camera frame.")
            continue

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (640, 480))
        results = selfie_segmentation.process(image)
        results1 = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(image, results1.pose_landmarks, mp_pose.POSE_CONNECTIONS, landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        lmList = []

        end = round(time.time(), 1)

        if ((end - start) == 0.5):
            for id, lm in enumerate(results1.pose_landmarks.landmark):
                h, w, c = image.shape
                print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

            start = round(time.time(), 1)

        # 사람 뒤에 있는 배경을 지워주는 작업
        condition = np.stack((results.segmentation_mask,) * 3, axis = -1) > 0.15

        # 만약 지정된 배경화면이 없을 경우
        if bg_image is None:
            bg_image = np.zeros(image.shape, dtype = np.uint8)
            bg_image[:] = BG_COLOR
        
        # 결과 이미지를 적용합니다
        output_image = np.where(condition, image, bg_image)

        cv2.imshow('MediaPipe Pose', cv2.flip(output_image, 1))

        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()

cv2.destroyAllWindows()