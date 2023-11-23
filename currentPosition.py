import cv2

cap = cv2.VideoCapture("easyDance.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
print(fps)
timestamps = [cap.get(cv2.CAP_PROP_POS_MSEC)]

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    timestamps = [cap.get(cv2.CAP_PROP_POS_MSEC)]

    print(timestamps)

    gray = cv2.resize(frame, (1366, 768))

    # Display the resulting frame
    cv2.imshow("Frame", gray)

    cv2.moveWindow("Frame", 0, 0)

    if cv2.waitKey(1) == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()