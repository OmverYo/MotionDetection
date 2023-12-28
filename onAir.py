import cv2, time
import poseModule as pm
import mysql.connector
import random

def distanceCalculate(p1, p2):
    """Calculate Euclidean distance between two points."""
    dis = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
    return dis

def air():
    user_cam = cv2.VideoCapture(0)
    detector = pm.poseDetector()

    mydb = mysql.connector.connect(host = "localhost", user = "root", password = "0000", database = "metaports")
    mycursor = mydb.cursor()

    randomCounter = random.randint(2, 5)

    Start = 0
    Count = 0

    # 점프 감지 임계값 설정
    JUMP_START_THRESHOLD = 25 # 이 값을 낮추면 낮게 점프해도 점프한걸로 간주
    JUMP_END_THRESHOLD = 20

    startTimer = time.time()
    endTimer = time.time()
    ankleInitialPosition = None
    anklePositionSet = False
    jumpStarted = False
    jumpStartTimer = 0

    sql = "INSERT INTO program_running (is_running) VALUES (1)"
    mycursor.execute(sql)
    mydb.commit()

    while user_cam.isOpened():
        success, image = user_cam.read()

        if not success:
            print("Ignoring empty camera frame.")
            continue

        try:
            image = detector.findPose(image)
            results = detector.findAnkle(image)
            handList_user = detector.findHand(image)

            sql = "UPDATE hand SET rx = %s, ry = %s, lx = %s, ly = %s WHERE hand_id = 1"
            mycursor.execute(sql, (handList_user[1][1], handList_user[1][2], handList_user[0][1], handList_user[0][2]))
            mydb.commit()

            leftAnkle = [results[0][1], results[0][2]]
            rightAnkle = [results[1][1], results[1][2]]

            # 초기 위치 설정
            if not anklePositionSet and time.time() - startTimer > 3:
                ankleInitialPosition = (leftAnkle, rightAnkle)
                anklePositionSet = True

            # 점프 감지
            if anklePositionSet:
                currentAnkleHeight = (leftAnkle[1] + rightAnkle[1]) / 2
                initialAnkleHeight = (ankleInitialPosition[0][1] + ankleInitialPosition[1][1]) / 2

                # 점프 시작 감지
                if not jumpStarted and currentAnkleHeight < initialAnkleHeight - JUMP_START_THRESHOLD:
                    jumpStarted = True
                    jumpStartTimer = time.time()

                # 점프 종료 감지
                elif jumpStarted and currentAnkleHeight > initialAnkleHeight - JUMP_END_THRESHOLD:
                    jumpEndTimer = time.time()
                    airTime = round((jumpEndTimer - jumpStartTimer), 3)
                    jumpStarted = False
                    print("Air Time:", airTime, "seconds")  # 체공시간 출력

                    sql = "INSERT INTO basic_data (reaction_time, on_air, squat_jump, knee_punch, balance_test) VALUES (0, 1.314, 0, 0, 0)"
                    mycursor.execute(sql)
                    mydb.commit()
        
        except:
            success, image = user_cam.read()
        
        ret_val, buffer = cv2.imencode('.jpg', image)

        image = buffer.tobytes()

        yield (b'--image\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')

    user_cam.release()