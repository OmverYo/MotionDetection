# import cv2

# cap = cv2.VideoCapture("C:/Users/pc/Desktop/poomse/TK_Poomsae_cheonkwon_C_FV.mp4")

# fps = round(cap.get(cv2.CAP_PROP_FPS), 0)
# total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
# timestamps = [cap.get(cv2.CAP_PROP_POS_MSEC)]

# print(fps)
# print(total_frames)
# print(timestamps)

# while cap.isOpened():
#     success, image = cap.read()

#     timestamps = [int(cap.get(cv2.CAP_PROP_POS_MSEC))]

#     print(timestamps)
        
# cap.release()
# cv2.destroyAllWindows()

# import cv2
# import mediapipe as mp
# import numpy as np
# mp_drawing = mp.solutions.drawing_utils
# mp_drawing_styles = mp.solutions.drawing_styles
# mp_pose = mp.solutions.pose

# # For webcam input:
# cap = cv2.VideoCapture("C:/Users/pc/Desktop/poomse/TK_Poomsae_cheonkwon_C_FV.mp4")
# with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
#   while cap.isOpened():
#     success, image = cap.read()
#     if not success:
#       print("Ignoring empty camera frame.")
#       # If loading a video, use 'break' instead of 'continue'.
#       continue

#     # To improve performance, optionally mark the image as not writeable to
#     # pass by reference.
#     image.flags.writeable = False
#     image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     results = pose.process(image)

#     # Draw the pose annotation on the image.
#     image.flags.writeable = True
#     image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
#     mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS, landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
#     # Flip the image horizontally for a selfie-view display.
#     cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
#     if cv2.waitKey(5) & 0xFF == 27:
#       break
# cap.release()

import pymysql
import paramiko

# SSH configuration
ssh_host = '175.106.97.249'
ssh_port = 22
ssh_username = 'root'
ssh_password = 'humanf1002~'

# MySQL database configuration
mysql_host = 'db-kl7j1-kr.vpc-pub-cdb.ntruss.com'
mysql_port = 3306
mysql_user = 'djlee_991'
mysql_password = 'HumanF_99!'
mysql_db = 'metaports'

# Create an SSH tunnel
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(ssh_host, ssh_port, ssh_username, ssh_password)

# Forward the local port to the remote MySQL server
ssh_tunnel = ssh_client.get_transport().open_channel('direct-tcpip', (mysql_host, mysql_port), ('db-kl7j1-kr.vpc-pub-cdb.ntruss.com', 3306))

# Connect to the MySQL database through the SSH tunnel
mysql_connection = pymysql.connect(
    host='db-kl7j1-kr.vpc-pub-cdb.ntruss.com',
    port=3306,
    user=mysql_user,
    password=mysql_password,
    database=mysql_db,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

# Perform MySQL operations
try:
    with mysql_connection.cursor() as cursor:
        # Example query
        sql = "SELECT * FROM hand;"
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
finally:
    mysql_connection.close()
    ssh_tunnel.close()
    ssh_client.close()