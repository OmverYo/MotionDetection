import cv2, time
import poseModule as pm
from scipy.spatial.distance import cosine
from fastdtw import fastdtw
# import json
import mysql.connector

mydb = mysql.connector.connect(host = "localhost", user = "root", password = "0000", database = "metaports")
mycursor = mydb.cursor()

# 데이터 베이스에서 가져올 정보를 입력합니다
sql = "SELECT * FROM coordinates"

# SQL 코드를 실행 합니다
mycursor.execute(sql)

# 실행한 SQL 코드의 출력 결과를 불러옵니다
myresult = mycursor.fetchall()

# 유저 캠은 플레이어의 모습이 보일 영상
user_cam = cv2.VideoCapture(0)

# 각 영상 별로 모션을 인식할 함수를 불러옵니다
detector_1 = pm.poseDetector()

# 정확도 값을 저장할 변수
accuracyList = []

# with open('data.json') as json_file:
#     json_data = json.load(json_file)

# FPS를 0으로 설정합니다
fps_time = 0

# 현재 프레임 수를 기록 합니다
frame_counter = 0

# 모션 인식 중 해당 정확도의 동작일 경우 해당 프레임 수를 저장합니다
awesome_frame = 0
great_frame = 0
good_frame = 0
ok_frame = 0
bad_frame = 0

# 좌표 값을 22개 마다 불러옵니다
a = 0
b = 22

while a < b:
    accuracyList.append(myresult[a])
    a += 1

start = round(time.time(), 1)
end = round(time.time(), 1)

# 대상으로 쓰일 영상이나 유저의 캠이 정상적으로 켜진 경우
while (user_cam.isOpened()):
    try:
        ret_val, image_1 = user_cam.read()

        # 이미지의 위치를 인식합니다
        image_1 = detector_1.findPose(image_1)
        lmList_user = detector_1.findPosition(image_1)

        # fastdtw의 모듈로 두 좌표를 코사인 유사도로 비교합니다
        error, _ = fastdtw(lmList_user, accuracyList, dist = cosine)

        # 현재 프로그램의 실행되는 프레임 수를 카운트 합니다
        frame_counter += 1

        end = round(time.time(), 1)

        # 해당 프레임의 동작 비교가 끝난 후 다음 프레임의 좌표 값으로 이동
        if ((end - start) == 1):
            # 정확도가 90% 이상일 경우 Awesome 프레임 수를 올립니다
            if error < 0.1:
                awesome_frame += 1

            # 정확도가 80% 이상일 경우 Great 프레임 수를 올립니다
            elif error < 0.2 and error > 0.1:
                great_frame += 1

            # 정확도가 70% 이상일 경우 Good 프레임 수를 올립니다
            elif error < 0.3 and error > 0.2:
                good_frame += 1

            # 정확도가 60% 이상일 경우 OK 프레임 수를 올립니다
            elif error < 0.4 and error > 0.3:
                ok_frame += 1

            # 정확도가 60% 미만일 경우 Bad 프레임 수를 올립니다
            elif error > 0.4:
                bad_frame += 1
            
            print("awesome", awesome_frame)
            print("great", great_frame)
            print("good", good_frame)
            print("ok", ok_frame)
            print("bad", bad_frame)
            b += 22
            accuracyList = []

            while a < b:
                accuracyList.append(myresult[a])
                a += 1

            start = round(time.time(), 1)

        if ((end - start) == 5):
            # 정확도 프레임 수를 총 프레임 수를 나누어 백분률로 표기
            print(int(((awesome_frame + great_frame + good_frame + ok_frame)/frame_counter) * 100))

    except:
        print("카메라에 인식할 대상이 없습니다")
        break

# 영상 종료 후 모든 창을 종료해줍니다
user_cam.release()
cv2.destroyAllWindows()