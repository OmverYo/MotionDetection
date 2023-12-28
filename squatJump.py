import cv2, time
import poseModule as pm
import mysql.connector
import random

def distanceCalculate(p1, p2):
    """p1 and p2 in format (x1, y1) and (x2, y2) tuples"""
    dis = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
    
    return dis

def squatJump():
    user_cam = cv2.VideoCapture(0)
    detector = pm.poseDetector()

    mydb = mysql.connector.connect(host = "localhost", user = "root", password = "0000", database = "metaports")
    mycursor = mydb.cursor()

    randomCounter = random.randint(2, 5)

    counterResult = []

    Start = 0
    Count = 0

    sql = "INSERT INTO program_running (is_running) VALUES (1)"
    mycursor.execute(sql)
    mydb.commit()

    startTimer = time.time()
    endTimer = time.time()

    while user_cam.isOpened():
        success, image = user_cam.read()
        
        try:
            image = detector.findPose(image)
            results = detector.findHip(image)

            handList_user = detector.findHand(image)

            sql = "UPDATE hand SET rx = %s, ry = %s, lx = %s, ly = %s WHERE hand_id = 1"
            mycursor.execute(sql, (handList_user[1][1], handList_user[1][2], handList_user[0][1], handList_user[0][2]))
            mydb.commit()

            leftHip = [results[0][1], results[0][2]]
            leftAnkle = [results[1][1], results[1][2]]

            if Count == 3:
                sql = "INSERT INTO program_running (is_running) VALUES (0)"
                mycursor.execute(sql)
                mydb.commit()

                y = 0

                for x in counterResult:
                    y += x

                y = round(y / 3, 3)

                sql = "INSERT INTO basic_data (reaction_time, on_air, squat_jump, knee_punch, balance_test) VALUES (0, 0, 10, 0, 0)"
                mycursor.execute(sql)
                mydb.commit()

                break

            if int(endTimer) - int(startTimer) >= randomCounter:
                print("GO")

                startTimer = time.time()

            if distanceCalculate(leftHip, leftAnkle) < 50:
                Start = 1
                endTimer = time.time()

            elif Start and distanceCalculate(leftHip, leftAnkle) > 100:
                endTimer = time.time()
                
                Count = Count + 1
                Start = 0

                counterResult.append(round((endTimer - startTimer), 3))
                print("Time Taken:", round((endTimer - startTimer), 3))

                randomCounter = random.randint(2, 5)

                print("Random:", randomCounter)
                print("Count:", Count)

                startTimer = time.time()

        except:
            success, image = user_cam.read()

        ret_val, buffer = cv2.imencode('.jpg', image)

        image = buffer.tobytes()

        yield (b'--image\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
        
    user_cam.release()