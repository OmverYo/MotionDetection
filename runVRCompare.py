import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial.distance import cosine
from fastdtw import fastdtw
import json
import time

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_selfie_segmentation = mp.solutions.selfie_segmentation
mp_pose = mp.solutions.pose

# 배경화면의 색상을 지정합니다
BG_COLOR = (0, 255, 0) # GREEN

# 정확도 값을 저장할 변수
json_data = []

with open('data.json') as json_file:
    json_data = json.load(json_file)

# FPS를 0으로 설정합니다
fps_time = 0

accuracyList = []

frame_counter = 0

# 모션 인식 중 올바른 동작일 경우 해당 프레임 수를 저장합니다
correct_frames = 0

cap = cv2.VideoCapture(0)

a = 0
b = 22

while a < b:
    accuracyList.append(json_data[a])
    a += 1

with mp_selfie_segmentation.SelfieSegmentation(model_selection = 0) as selfie_segmentation, mp_pose.Pose(model_complexity = 0, min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:
    # 배경화면의 이미지를 설정 할 수 있으나 없음으로 설정
    bg_image = None

    start = round(time.time(), 1)
    
    while cap.isOpened():
        success, image = cap.read()

        if not success:
            print("Ignoring empty camera frame.")
            continue

        image = cv2.flip(image, 1)

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (640, 480))
        results = selfie_segmentation.process(image)
        results1 = pose.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        lmList = []

        end = round(time.time(), 1)

        if (True):
            for id, lm in enumerate(results1.pose_landmarks.landmark):
                if id not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                    h, w, c = image.shape
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

        fps_time = time.time()

        error, _ = fastdtw(lmList, accuracyList, dist = cosine)

        # 두 이미지를 비교하여 다른 값을 표시합니다
        cv2.putText(output_image, 'Error: {}%'.format(str(round(100*(float(error)),2))), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # 정화도가 90% 가 넘을 경우 정확한 동작으로 표시합니다
        if error < 0.15:
            cv2.putText(output_image, "CORRECT STEPS", (40, 440), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            # 정확도를 측정 후 정확도 프레임 수를 1개 올립니다
            correct_frames += 1
        
        # 틀렸을 경우 틀린 동작으로 표시합니다
        else:
            cv2.putText(output_image, "INCORRECT STEPS", (40, 440), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # 초당 프레임 수를 표시합니다
        cv2.putText(output_image, "FPS: %f" % (1.0 / (time.time() - fps_time)), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # 유저의 캠 프레임 수를 측정합니다
        if frame_counter == 0:
            frame_counter = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        # 올바른 동작 프레임 수를 총 플레이 타임 프레임 수를 나눠 백분율로 표기합니다
        cv2.putText(output_image, "Dance Steps Accurately Done: {}%".format(str(round(100*correct_frames/frame_counter, 2))), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

        cv2.imshow('MediaPipe Pose', output_image)
        
        if (True):
                b += 23
                accuracyList = []

                while a < b:
                    accuracyList.append(json_data[a])
                    a += 1
                
                start = round(time.time(), 1)
                frame_counter = 0
        
        if cv2.waitKey(5) & 0xFF == 27:
            break

cap.release()

cv2.destroyAllWindows()