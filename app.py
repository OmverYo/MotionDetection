from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import numpy as np
import poseModule as pm
from scipy.spatial.distance import cosine
from fastdtw import fastdtw

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_selfie_segmentation = mp.solutions.selfie_segmentation
mp_pose = mp.solutions.pose

# 배경화면의 색상을 지정합니다
BG_COLOR = (0, 255, 0) # GREEN

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def generate_frames():
    with mp_selfie_segmentation.SelfieSegmentation(model_selection = 0) as selfie_segmentation, mp_pose.Pose(model_complexity = 0, min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:
        bg_image = None
        
        while True:
            success, image = camera.read()
            if not success:
                break
            else:
                results = selfie_segmentation.process(image)
                results1 = pose.process(image)

                condition = np.stack((results.segmentation_mask,) * 3, axis = -1) > 0.15

                # 만약 지정된 배경화면이 없을 경우
                if bg_image is None:
                    bg_image = np.zeros(image.shape, dtype = np.uint8)
                    bg_image[:] = BG_COLOR
                
                # 결과 이미지를 적용합니다
                output_image = np.where(condition, image, bg_image)
                ret, buffer = cv2.imencode('.jpg', output_image)

                output_image = buffer.tobytes()
                yield (b'--image\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + output_image + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=image')

if __name__ == '__main__':
    app.run(debug=True)