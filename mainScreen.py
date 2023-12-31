import cv2
import poseModule as pm
import api

def mainScreen():
    user_cam = cv2.VideoCapture(0)
    detector = pm.poseDetector()

    while user_cam.isOpened():
        try:
            ret_val, image_1 = user_cam.read()

            image_1 = detector.findPose(image_1)
            handList_user = detector.findHand(image_1)
            value = [handList_user[1][1], handList_user[1][2], handList_user[0][1], handList_user[0][2]]

            api.gamedata_api("/HandData/1", "PUT", value)

            ret_val, buffer = cv2.imencode('.jpg', image_1)

            image_1 = buffer.tobytes()

            yield (b'--image\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + image_1 + b'\r\n')
        
        except:
            pass

    user_cam.release()