from flask import Flask, render_template, Response
import cv2, time
import mediapipe as mp
import numpy as np
from scipy.spatial.distance import cosine
from fastdtw import fastdtw
import mysql.connector

app = Flask(__name__)

def generate_frames():
    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    mp_pose = mp.solutions.pose

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

    # 정확도 좌표 값을 저장할 변수
    accuracyList = []

    # 정확도 최종 점수 보관 리스트
    totalAccuracyList = []

    # 현재 프레임 수를 기록 합니다
    capture_time = 0

    # 모션 인식 중 해당 정확도의 동작일 경우 해당 프레임 수를 저장합니다
    perfect_frame = 0
    awesome_frame = 0
    good_frame = 0
    ok_frame = 0
    bad_frame = 0

    # 좌표 값을 22개 마다 불러옵니다
    a = 0
    b = 22

    while a < b:
        accuracyList.append(myresult[a])
        a += 1

    print("Ready")

    start = round(time.time(), 1)
    end = round(time.time(), 1)

    # 배경화면의 색상을 지정합니다
    BG_COLOR = (0, 255, 0) # GREEN

    with mp_selfie_segmentation.SelfieSegmentation(model_selection = 0) as selfie_segmentation, mp_pose.Pose(model_complexity = 0, min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:
        while user_cam.isOpened():
            try:
                ret_val, image_1 = user_cam.read()

                results = selfie_segmentation.process(image_1)
                results1 = pose.process(image_1)

                end = round(time.time(), 1)

                lmList_user = []

                if end - start >= 1:
                    for id, lm in enumerate(results1.pose_landmarks.landmark):
                        if id not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                            h, w, c = image_1.shape
                            cx, cy = int(lm.x * w), int(lm.y * h)
                            lmList_user.append([id, cx, cy])

                # fastdtw의 모듈로 두 좌표를 코사인 유사도로 비교합니다
                error, _ = fastdtw(lmList_user, accuracyList, dist = cosine)

                if end - start >= 1:
                # 정확도가 95% 이상일 경우 Pefect 프레임 수를 올립니다
                    if error < 0.05:
                        perfect_frame += 1

                    # 정확도가 85% ~ 95% 경우 Awesome 프레임 수를 올립니다
                    elif error < 0.15 and error > 0.05:
                        awesome_frame += 1

                    # 정확도가 70% ~ 84% 경우 Good 프레임 수를 올립니다
                    elif error < 0.3 and error > 0.16:
                        good_frame += 1

                    # 정확도가 50% ~ 69% 경우 OK 프레임 수를 올립니다
                    elif error < 0.5 and error > 0.31:
                        ok_frame += 1

                    # 정확도가 50% 미만일 경우 Bad 프레임 수를 올립니다
                    elif error > 0.5:
                        bad_frame += 1
                    
                    capture_time += 1

                    print("")
                    print("perfect", perfect_frame)
                    print("awesome", awesome_frame)
                    print("good", good_frame)
                    print("ok", ok_frame)
                    print("bad", bad_frame)

                    if error > 1:
                        error = 1
                        totalAccuracyList.append((capture_time, int((1 - error) * 100)))

                    print("Total", totalAccuracyList[-1])

                    print("correct", int(((perfect_frame + awesome_frame + good_frame + ok_frame)/capture_time) * 100))

                    print(capture_time)

                    b += 22
                    accuracyList = []

                    while a < b:
                        accuracyList.append(myresult[a])
                        a += 1

                    sql = "INSERT INTO mt_training_result (capture_time, accuracy) VALUES (%s, %s)"
                    mycursor.execute(sql, totalAccuracyList[-1])
                    mydb.commit()

                    start = round(time.time(), 1)

                condition = np.stack((results.segmentation_mask,) * 3, axis = -1) > 0.15

                bg_image = cv2.imread("picture1233.jpg")

                # 만약 지정된 배경화면이 없을 경우
                if bg_image is None:
                    bg_image = np.zeros(image_1.shape, dtype = np.uint8)
                    bg_image[:] = BG_COLOR
                
                # 결과 이미지를 적용합니다
                output_image = np.where(condition, image_1, bg_image)
                ret, buffer = cv2.imencode('.jpg', output_image)

                output_image = buffer.tobytes()
                yield (b'--image_1\r\n'
                    b'Content-Type: image_1/jpeg\r\n\r\n' + output_image + b'\r\n')
                
            except:
                print("비교 모듈이 종료됩니다")
                break

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=image_1')

if __name__ == '__main__':
    app.run(debug=True)