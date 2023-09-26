import cv2
import time

# we create a script that runs the webcam and pressing "q" will stop it

video = cv2.VideoCapture(0)
time.sleep(1)

while True:
    check1, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # converting to grayscale pixels
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)
    cv2.imshow("My video", gray_frame_gau)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break


video.release()
