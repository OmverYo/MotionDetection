import sys
import cv2
import mediapipe as mp
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer, Qt

mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation

class WebcamWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)

    def initUI(self):
        self.setGeometry(100, 100, 640, 480)  # 창 위치와 크기 설정
        self.setWindowTitle('Webcam')
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 640, 480)  # 라벨 위치와 크기 설정

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(20)

        self.cap = cv2.VideoCapture(0)

    def updateFrame(self):
        ret, frame = self.cap.read()
        if ret:
            # OpenCV 처리
            frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
            frame.flags.writeable = False
            results = self.segmentation.process(frame)
            frame.flags.writeable = True

            alpha_channel = np.ones(frame.shape[:2], dtype=frame.dtype) * 255  # Full alpha
            bg_image = np.dstack((frame, alpha_channel))
            mask = results.segmentation_mask > 0.1
            bg_image[..., 3] = np.where(mask, 255, 0)

            # PyQT로 이미지 표시
            h, w, ch = bg_image.shape
            bytesPerLine = ch * w
            convertToQtFormat = QImage(bg_image.data, w, h, bytesPerLine, QImage.Format_RGBA8888)
            p = convertToQtFormat.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio)
            self.label.setPixmap(QPixmap.fromImage(p))
    
    def closeEvent(self, event):
        # 창이 닫힐 때 리소스 해제
        self.cap.release()
        self.segmentation.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = WebcamWidget()
    ex.show()
    sys.exit(app.exec_())
