import cv2
import mediapipe as mp

class poseDetector():
    # 클라스 안에 담아 저장해줄 변수를 만들어줍니다
    def __init__(self, mode = False, upBody = False, smooth = True, detectionCon = 0.85, trackCon = 0.85):
        self.mode = mode
        self.upBody = upBody
        self.smooth = smooth
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(self.mode, min_detection_confidence = 0.5, min_tracking_confidence = 0.5)

    # 보여지는 이미지 위에 점과 선을 이어 스켈레톤을 만들어줍니다
    def findPose(self, img, draw = True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks, self.mpPose.POSE_CONNECTIONS)
        return img

    # 보여지는 이미지를 인식하고 신체의 각 부위를 33개의 점으로 지정하여 행렬로 저장해줍니다
    def findPosition(self, img, draw = True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList