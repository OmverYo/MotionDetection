import cv2, time
import poseModule as pm
import mysql.connector

def balanceTest():
    # 초기 위치 설정 및 준비 시간 계산을 위한 변수
    initialPositionSet = False
    balanceStarted = False
    balanceStartTime = 0

    print("정자세로 서서 준비하세요. 3초 후에 시작합니다.")
    prepStartTime = time.time()

    user_cam = cv2.VideoCapture(0)
    detector = pm.poseDetector()

    mydb = mysql.connector.connect(host = "localhost", user = "root", password = "0000", database = "metaports")
    mycursor = mydb.cursor()

    sql = "INSERT INTO program_running (is_running) VALUES (1)"
    mycursor.execute(sql)
    mydb.commit()

    startTimer = time.time()
    endTimer = time.time()

    while user_cam.isOpened():
        success, image = user_cam.read()

        if not success:
            print("Ignoring empty camera frame.")
            continue

        try:
            image = detector.findPose(image)
            results = detector.findKneeHip(image)

            handList_user = detector.findHand(image)

            sql = "UPDATE hand SET rx = %s, ry = %s, lx = %s, ly = %s WHERE hand_id = 1"
            mycursor.execute(sql, (handList_user[1][1], handList_user[1][2], handList_user[0][1], handList_user[0][2]))
            mydb.commit()

            leftHip = [results[0][0], results[0][1]]
            leftKnee = [results[1][0], results[1][1]]

            if not initialPositionSet and time.time() - prepStartTime > 3:
                initialKneeHipDistance = abs(leftKnee[1] - leftHip[1])
                initialPositionSet = True
                print("평형성 측정을 시작합니다.")

            if initialPositionSet and not balanceStarted:
                currentKneeHipDistance = abs(leftKnee[1] - leftHip[1])
                if currentKneeHipDistance < initialKneeHipDistance - 10:  # 무릎과 허리 사이의 거리가 좁아졌을 때 (측정 시작 임계값. 이 값이 클수록 더 큰 움직임을 필요로 함)
                    balanceStartTime = time.time()
                    balanceStarted = True

            if balanceStarted:
                currentKneeHipDistance = abs(leftKnee[1] - leftHip[1])
                if currentKneeHipDistance > initialKneeHipDistance - 3:  # 무릎과 허리 사이의 거리가 다시 늘어났을 때 (무너진 것으로 간주되는 임계값. 이 값이 클수록 더 민감하게 반응)
                    balanceTime = time.time() - balanceStartTime

                    print("평형 유지 시간:", round(balanceTime, 3), "초")

                    sql = "INSERT INTO program_running (is_running) VALUES (0)"
                    mycursor.execute(sql)
                    mydb.commit()

                    sql = "INSERT INTO basic_data (reaction_time, on_air, squat_jump, knee_punch, balance_test) VALUES (0, 0, 0, 0, 10)"
                    mycursor.execute(sql)
                    mydb.commit()

                    break
        except:
            success, image = user_cam.read()

        ret_val, buffer = cv2.imencode('.jpg', image)

        image = buffer.tobytes()

        yield (b'--image\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
        
    user_cam.release()