import cv2
import mediapipe as mp
# import time
from tkinter import *
from PIL import Image, ImageTk

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

window = Tk()  #Makes main window
window.overrideredirect(True)
window.wm_attributes("-topmost", True)
window.geometry("+600+200")
display1 = Label(window)
display1.grid(row = 1, column = 0, padx = 0, pady = 0)  #Display 1

cap = cv2.VideoCapture(0)

# frame_counter = 0

# start = round(time.time(), 1)

def move():
    x, y = window.winfo_pointerxy()
    window.geometry(f"+{x}+{y}")

def show_frame():
    with mp_pose.Pose(model_complexity = 0, min_detection_confidence = 0.5, min_tracking_confidence = 0.5) as pose:
        success, image = cap.read()

        image = cv2.resize(image, (800, 600))
        image = cv2.flip(image, 1)

        # 필요에 따라 성능 향상을 위해 이미지 작성을 불가능함으로 기본 설정합니다.
        # image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        # 포즈 주석을 이미지 위에 그립니다.
        # image.flags.writeable = True
        # image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, landmark_drawing_spec = mp_drawing_styles.get_default_pose_landmarks_style())

        img = Image.fromarray(image)
        imgtk = imgtk = ImageTk.PhotoImage(master = display1, image = img)

        display1.imgtk = imgtk #Shows frame for display 1
        display1.configure(image = imgtk)
        
        window.after(10, show_frame)


        # end = round(time.time(), 1)

        # lmList = []

        # if (end - start == 0.5):
        #     for id, lm in enumerate(results.pose_landmarks.landmark):
        #         h, w, c = image.shape
        #         print(id, lm)
        #         cx, cy = int(lm.x * w), int(lm.y * h)
        #         lmList.append([id, cx, cy])

        #         start = round(time.time(), 1)
        
        # 보기 편하게 이미지를 좌우 반전합니다.
        # cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))

show_frame()
window.mainloop()
# cap.release()

# cv2.destroyAllWindows()