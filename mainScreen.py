import cv2
import poseModule as pm
import mysql.connector

def mainScreen():
    user_cam = cv2.VideoCapture(0)
    detector = pm.poseDetector()

    mydb = mysql.connector.connect(host = "localhost", user = "root", password = "0000", database = "metaports")
    mycursor = mydb.cursor()

    while user_cam.isOpened():
        try:
            ret_val, image_1 = user_cam.read()

            image_1 = detector.findPose(image_1)
            handList_user = detector.findHand(image_1)

            sql = "UPDATE hand SET rx = %s, ry = %s, lx = %s, ly = %s WHERE hand_id = 1"
            mycursor.execute(sql, (handList_user[1][1], handList_user[1][2], handList_user[0][1], handList_user[0][2]))
            mydb.commit()

            ret_val, buffer = cv2.imencode('.jpg', image_1)

            image_1 = buffer.tobytes()

            yield (b'--image\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + image_1 + b'\r\n')
        
        except:
            pass