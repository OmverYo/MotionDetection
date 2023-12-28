import cv2
import mediapipe as mp
import time

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)

# 초기 위치 설정 및 준비 시간 계산을 위한 변수
initialPositionSet = False
balanceStarted = False
balanceStartTime = 0

print("정자세로 서서 준비하세요. 3초 후에 시작합니다.")
prepStartTime = time.time()

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    try:
        results = pose.process(image)
        image_height, image_width, _ = image.shape

        if results.pose_landmarks:
            knee = (int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE.value].x * image_width), 
                    int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE.value].y * image_height))
            hip = (int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP.value].x * image_width), 
                int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP.value].y * image_height))

            if not initialPositionSet and time.time() - prepStartTime > 3:
                initialKneeHipDistance = abs(knee[1] - hip[1])
                initialPositionSet = True
                print("평형성 측정을 시작합니다.")

            if initialPositionSet and not balanceStarted:
                currentKneeHipDistance = abs(knee[1] - hip[1])
                if currentKneeHipDistance < initialKneeHipDistance - 10:  # 무릎과 허리 사이의 거리가 좁아졌을 때 (측정 시작 임계값. 이 값이 클수록 더 큰 움직임을 필요로 함)
                    balanceStartTime = time.time()
                    balanceStarted = True

            if balanceStarted:
                currentKneeHipDistance = abs(knee[1] - hip[1])
                if currentKneeHipDistance > initialKneeHipDistance - 3:  # 무릎과 허리 사이의 거리가 다시 늘어났을 때 (무너진 것으로 간주되는 임계값. 이 값이 클수록 더 민감하게 반응)
                    balanceTime = time.time() - balanceStartTime
                    print("평형 유지 시간:", round(balanceTime, 3), "초")
                    break
    except:
        success, image = cap.read()

    cv2.imshow('MediaPipe Pose', image)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()