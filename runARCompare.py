import cv2, time
import poseModule as pm
from scipy.spatial.distance import cosine
from fastdtw import fastdtw
import json

# 유저 캠은 플레이어의 모습이 보일 영상
user_cam = cv2.VideoCapture(0)

# 각 영상 별로 모션을 인식할 함수를 불러옵니다
detector_1 = pm.poseDetector()

# 정확도 값을 저장할 변수
json_data = []

with open('data.json') as json_file:
    json_data = json.load(json_file)

accuracyList = []

# FPS를 0으로 설정합니다
fps_time = 0

frame_counter = 0

# 모션 인식 중 올바른 동작일 경우 해당 프레임 수를 저장합니다
correct_frames = 0

a = 0
b = 22

while a < b:
    accuracyList.append(json_data[a])
    a += 1

start = round(time.time(), 1)

# 대상으로 쓰일 영상이나 유저의 캠이 정상적으로 켜진 경우
while (user_cam.isOpened()):
    try:
        ret_val, image_1 = user_cam.read()
        
        # 해당 창을 특정 크기로 재설정합니다
        image_1 = cv2.resize(image_1, (640, 480))
        # 유저의 영상을 좌우 반전하여 거울 모드로 합니다
        # image_1 = cv2.flip(image_1, 1)
        image_1 = detector_1.findPose(image_1)
        # 이미지의 위치를 인식합니다
        lmList_user = detector_1.findPosition(image_1)

        # 모든 작업이 지나온 후 초당 프레임 수를 1개 올립니다
        frame_counter += 1

        if ret_val:
            # 유저의 영상과 모델의 영상을 코사인 유사도로 비교합니다
            error, _ = fastdtw(lmList_user, accuracyList, dist = cosine)

            # 두 이미지를 비교하여 다른 값을 표시합니다
            # cv2.putText(image_1, 'Error: {}%'.format(str(round(100*(float(error)),2))), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # 정화도가 90% 가 넘을 경우 정확한 동작으로 표시합니다
            # if error < 0.15:
            #     cv2.putText(image_1, "CORRECT STEPS", (40, 440), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            #     # 정확도를 측정 후 정확도 프레임 수를 1개 올립니다
            #     correct_frames += 1
            
            # # 틀렸을 경우 틀린 동작으로 표시합니다
            # else:
            #     cv2.putText(image_1, "INCORRECT STEPS", (40, 440), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # 초당 프레임 수를 표시합니다
            # cv2.putText(image_1, "FPS: %f" % (1.0 / (time.time() - fps_time)), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # 유저의 캠 프레임 수를 측정합니다
            if frame_counter == 0:
                frame_counter = user_cam.get(cv2.CAP_PROP_FRAME_COUNT)

            # 올바른 동작 프레임 수를 총 플레이 타임 프레임 수를 나눠 백분율로 표기합니다
            # cv2.putText(image_1, "Dance Steps Accurately Done: {}%".format(str(round(100*correct_frames/frame_counter, 2))), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

            # 모델의 영상과 플레이어의 영상을 출력시킵니다
            # cv2.imshow("User Video", image_1)

            fps_time = time.time()

            end = round(time.time(), 1)

            if (True):
                b += 23
                accuracyList = []

                while a < b:
                    accuracyList.append(json_data[a])
                    a += 1
                
                start = round(time.time(), 1)
                frame_counter = 0

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    except:
        print("카메라에 인식할 대상이 없습니다")
        break

# 영상 종료 후 모든 창을 종료해줍니다
user_cam.release()
cv2.destroyAllWindows()