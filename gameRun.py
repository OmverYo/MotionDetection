import cv2, time, json
import numpy as np
import mediapipe as mp
import poseModule as pm
from scipy.spatial.distance import cosine
from fastdtw import fastdtw
import mysql.connector
import pathlib

def gameRun():
    path = str(pathlib.Path(__file__).parent.resolve()).replace("\\", "/") + "/"

    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection = 0)

    mydb = mysql.connector.connect(host = "localhost", user = "root", password = "0000", database = "metaports")
    mycursor = mydb.cursor()

    user_cam = cv2.VideoCapture(0)

    detector = pm.poseDetector()

    totalAccuracyList = []

    capture_time = 0

    perfect_frame = 0
    awesome_frame = 0
    good_frame = 0
    ok_frame = 0
    bad_frame = 0

    is_vr = False

    sql = "SELECT * FROM background"

    mycursor.execute(sql)

    result = mycursor.fetchall()

    myVR = result[-1][1]
    bg_name = result[-1][2]
    coord_name = result[-1][3]

    if myVR == 1:
        is_vr = True

    else:
        is_vr = False
    
    with open(f"{path}taekwondo_action/{coord_name}.json") as json_file:
        json_data = json.load(json_file)

    accuracyList = []

    a = 0
    b = 22

    while a < b:
        accuracyList.append(json_data[a])
        a += 1
    
    sql = "TRUNCATE TABLE background"
    mycursor.execute(sql)
    mydb.commit()

    sql = "INSERT INTO program_running (is_running) VALUES (1)"
    mycursor.execute(sql)
    mydb.commit()

    start = round(time.time(), 1)
    end = round(time.time(), 1)

    while user_cam.isOpened():
        try:
            ret_val, image_1 = user_cam.read()

            image_1 = detector.findPose(image_1)
            lmList_user = detector.findPosition(image_1)
            handList_user = detector.findHand(image_1)

            sql = "UPDATE hand SET rx = %s, ry = %s, lx = %s, ly = %s WHERE hand_id = 1"
            mycursor.execute(sql, (handList_user[1][1], handList_user[1][2], handList_user[0][1], handList_user[0][2]))
            mydb.commit()

            error, _ = fastdtw(lmList_user, accuracyList, dist = cosine)

            end = round(time.time(), 1)

            if end - start >= 1:
                if error < 0.05:
                    perfect_frame += 1

                elif error < 0.15 and error > 0.05:
                    awesome_frame += 1

                elif error < 0.3 and error > 0.16:
                    good_frame += 1

                elif error < 0.5 and error > 0.31:
                    ok_frame += 1

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
                    accuracyList.append(json_data[a])
                    a += 1
                
                sql = "INSERT INTO mt_training_result (capture_time, accuracy) VALUES (%s, %s)"
                mycursor.execute(sql, totalAccuracyList[-1])
                mydb.commit()

                start = round(time.time(), 1)

            if is_vr == True:
                
                results = selfie_segmentation.process(image_1)
                
                condition = np.stack((results.segmentation_mask,) * 3, axis = -1) > 0.15
                
                bg_image = cv2.imread(f"{path}{bg_name}")
                
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