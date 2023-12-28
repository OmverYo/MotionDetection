import cv2, time
import poseModule as pm
import mysql.connector

end = int(time.time())
start = int(time.time())

def distanceCalculate(p1, p2):
    """p1 and p2 in format (x1, y1) and (x2, y2) tuples"""
    dis = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
    
    return dis

def kneePunch():
    user_cam = cv2.VideoCapture(0)
    detector = pm.poseDetector()

    mydb = mysql.connector.connect(host = "localhost", user = "root", password = "0000", database = "metaports")
    mycursor = mydb.cursor()

    leftStart = 0
    rightStart = 0
    Count = 0

    sql = "INSERT INTO program_running (is_running) VALUES (1)"
    mycursor.execute(sql)
    mydb.commit()

    while user_cam.isOpened():
        success, image = user_cam.read()
        
        try:
            image = detector.findPose(image)
            results = detector.findKnee(image)

            handList_user = detector.findHand(image)

            sql = "UPDATE hand SET rx = %s, ry = %s, lx = %s, ly = %s WHERE hand_id = 1"
            mycursor.execute(sql, (handList_user[1][1], handList_user[1][2], handList_user[0][1], handList_user[0][2]))
            mydb.commit()

            leftShoulder = [results[0][1], results[0][2]]
            rightShoulder = [results[1][1], results[1][2]]
            leftWrist = [results[2][1], results[2][2]]
            rightWrist = [results[3][1], results[3][2]]
            leftKnee = [results[4][1], results[4][2]]
            rightKnee = [results[5][1], results[5][2]]

            if distanceCalculate(leftShoulder, leftWrist) < 65 and distanceCalculate(rightShoulder, rightKnee) > 155:
                leftStart = 1

            elif leftStart and distanceCalculate(leftShoulder, leftWrist) > 75 and distanceCalculate(rightShoulder, rightKnee) < 120:
                Count = Count + 1
                leftStart = 0

                print("Count:", Count)

            if distanceCalculate(rightShoulder, rightWrist) < 40 and distanceCalculate(leftShoulder, leftKnee) > 145:
                rightStart = 1

            elif rightStart and distanceCalculate(rightShoulder, rightWrist) > 95 and distanceCalculate(leftShoulder, leftKnee) < 130:
                Count = Count + 1
                rightStart = 0

                print("Count:", Count)

        except:
            success, image = user_cam.read()

        ret_val, buffer = cv2.imencode('.jpg', image)

        image = buffer.tobytes()

        yield (b'--image\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')
    
    sql = "INSERT INTO basic_data (reaction_time, on_air, squat_jump, knee_punch, balance_test) VALUES (0, 0, 0, 5, 0)"
    mycursor.execute(sql)
    mydb.commit()

    user_cam.release()