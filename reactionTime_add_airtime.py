import cv2
import mediapipe as mp
import time
import random

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def distanceCalculate(p1, p2):
    """Calculate Euclidean distance between two points."""
    dis = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
    return dis

randomCounter = random.randint(2, 5)

Start = 0
Count = 0

# 점프 감지 임계값 설정
JUMP_START_THRESHOLD = 25 # 이 값을 낮추면 낮게 점프해도 점프한걸로 간주
JUMP_END_THRESHOLD = 20

cap = cv2.VideoCapture(0)

startTimer = time.time()
endTimer = time.time()
ankleInitialPosition = None
anklePositionSet = False
jumpStarted = False
jumpStartTimer = 0

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    try:
        results = pose.process(image)
        image_height, image_width, _ = image.shape

        if results.pose_landmarks:
            leftAnkle = (int(results.pose_landmarks.landmark[27].x * image_width), int(results.pose_landmarks.landmark[27].y * image_height))
            rightAnkle = (int(results.pose_landmarks.landmark[28].x * image_width), int(results.pose_landmarks.landmark[28].y * image_height))

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
    except:
        success, image = cap.read()
    
    
    cv2.imshow('MediaPipe Pose', image)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()