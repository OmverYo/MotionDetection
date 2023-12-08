from flask import Flask, render_template, Response
import cv2, time
import numpy as np
import mediapipe as mp
import poseModule as pm
from scipy.spatial.distance import cosine
from fastdtw import fastdtw
import mysql.connector
import pathlib

app = Flask(__name__)

def generate_frames():
    path = str(pathlib.Path(__file__).parent.resolve()).replace("\\", "/") + "/"

    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection = 0)

    mydb = mysql.connector.connect(host = "localhost", user = "root", password = "0000", database = "metaports")
    mycursor = mydb.cursor()

    # 데이터 베이스에서 가져올 정보를 입력합니다
    sql = "SELECT * FROM coordinates"

    # SQL 코드를 실행 합니다
    mycursor.execute(sql)

    # 실행한 SQL 코드의 출력 결과를 불러옵니다
    myList = mycursor.fetchall()

    # 유저 캠은 플레이어의 모습이 보일 영상
    user_cam = cv2.VideoCapture(0)

    # 각 영상 별로 모션을 인식할 함수를 불러옵니다
    detector = pm.poseDetector()

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
        accuracyList.append(myList[a])
        a += 1
    
    is_vr = False

     # 데이터 베이스에서 가져올 정보를 입력합니다
    sql = "SELECT * FROM background"

    # SQL 코드를 실행 합니다
    mycursor.execute(sql)

    # 실행한 SQL 코드의 출력 결과를 불러옵니다
    myresult = mycursor.fetchall()[-1][1]

    if myresult == 1:
        is_vr = True

    else:
        is_vr = False

    sql = "TRUNCATE TABLE background"
    mycursor.execute(sql)
    mydb.commit()

    sql = "INSERT INTO program_running (is_running) VALUES (1)"
    mycursor.execute(sql)
    mydb.commit()

    start = round(time.time(), 1)
    end = round(time.time(), 1)

    # 대상으로 쓰일 영상이나 유저의 캠이 정상적으로 켜진 경우
    while user_cam.isOpened():
        try:
            ret_val, image_1 = user_cam.read()

            # 이미지의 위치를 인식합니다
            image_1 = detector.findPose(image_1)
            lmList_user = detector.findPosition(image_1)

            # fastdtw의 모듈로 두 좌표를 코사인 유사도로 비교합니다
            error, _ = fastdtw(lmList_user, accuracyList, dist = cosine)

            end = round(time.time(), 1)

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
                    accuracyList.append(myList[a])
                    a += 1
                
                sql = "INSERT INTO mt_training_result (capture_time, accuracy) VALUES (%s, %s)"
                mycursor.execute(sql, totalAccuracyList[-1])
                mydb.commit()

                # # isRunning 겟 한번
                # # 데이터 베이스에서 가져올 정보를 입력합니다
                # sql = "SELECT * FROM program_running"
                # # SQL 코드를 실행 합니다
                # mycursor.execute(sql)
                # # 실행한 SQL 코드의 출력 결과를 불러옵니다
                # myresult = mycursor.fetchall()[-1][1]
                
                # if myresult == 0:
                #     break

                start = round(time.time(), 1)

            if is_vr == True:
                
                results = selfie_segmentation.process(image_1)
                
                condition = np.stack((results.segmentation_mask,) * 3, axis = -1) > 0.15
                
                bg_image = cv2.imread(f"{path}picture1233.jpg")
                
                output_image = np.where(condition, image_1, bg_image)
                
                ret, buffer = cv2.imencode('.jpg', output_image)
                
                output_image = buffer.tobytes()
                yield (b'--image_1\r\n'
                    b'Content-Type: image_1/jpeg\r\n\r\n' + output_image + b'\r\n')
            
            else:
                ret_val, buffer = cv2.imencode('.jpg', image_1)

                image_1 = buffer.tobytes()

                yield (b'--image\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + image_1 + b'\r\n')
        except:
            print("비교 모듈이 종료됩니다")

            sql = "TRUNCATE TABLE program_running"
            mycursor.execute(sql)
            mydb.commit()

            break

    user_cam.release()

    if len(totalAccuracyList) != 0:
        total = 0

        for x in range(0, len(totalAccuracyList)):
            total = total + totalAccuracyList[x][1]

        total = int(total / len(totalAccuracyList))

        sql = "INSERT INTO player_data (total, perfect_frame, awesome_frame, good_frame, ok_frame, bad_frame) VALUES (%s, %s, %s, %s, %s, %s)"
        mycursor.execute(sql, (total, perfect_frame, awesome_frame, good_frame, ok_frame, bad_frame))
        mydb.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=image')

if __name__ == '__main__':
    mydb = mysql.connector.connect(host = "localhost", user = "root", password = "0000", database = "metaports")

    if not mydb:
        exit()
    
    app.run(debug=True)