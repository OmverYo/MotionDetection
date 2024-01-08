import cv2, time, json
import numpy as np
import mediapipe as mp
import poseModule as pm
from scipy.spatial.distance import cosine
from fastdtw import fastdtw
import pathlib
import api

def gameRun():
    path = str(pathlib.Path(__file__).parent.resolve()).replace("\\", "/") + "/"

    mp_selfie_segmentation = mp.solutions.selfie_segmentation
    selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection = 0)

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

    result = api.gamedata_api("/BackgroundData", "GET", None)

    result = result.replace("\"", "").replace("{", "").replace("}", "").replace(":", " ").replace(",", " ").split(" ")

    myVR = result[3]
    bg_name = result[5]
    coord_name = result[7]

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
    
    api.gamedata_api("/BackgroundData", "DELETE", None)

    api.gamedata_api("/ProgramData", "POST", True)

    start = round(time.time(), 1)
    end = round(time.time(), 1)

    while user_cam.isOpened():
        try:
            ret_val, image_1 = user_cam.read()

            image_1 = detector.findPose(image_1)
            lmList_user = detector.findPosition(image_1)
            handList_user = detector.findHand(image_1)

            value = [handList_user[1][1], handList_user[1][2], handList_user[0][1], handList_user[0][2]]

            api.gamedata_api("/HandData/1", "PUT", value)

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
                
                value = [totalAccuracyList[-1][0], totalAccuracyList[-1][1], 0]

                api.gamedata_api("/GameData", "POST", value)

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

            api.gamedata_api("/ProgramData", "DELETE", None)

            break

    user_cam.release()

    if len(totalAccuracyList) != 0:
        total = 0

        for x in range(0, len(totalAccuracyList)):
            total = total + totalAccuracyList[x][1]

        total = int(total / len(totalAccuracyList))

        value = [total, perfect_frame, awesome_frame, good_frame, ok_frame, bad_frame]

        api.gamedata_api("/PlayerData", "POST", value)