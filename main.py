import cv2
import time

# we create a script that runs the webcam and pressing "q" will stop it

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
while True:
    check1, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # converting to grayscale pixels
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
    cv2.imshow("My video", delta_frame)
    print(delta_frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break


video.release()
