import cv2
import time

# we create a script that runs the webcam and pressing "q" will stop it

video = cv2.VideoCapture(0)
time.sleep(1)

while True:
    check1, frame = video.read()
    cv2.imshow("My video", frame)

    key = cv2.waitKey(1)

    if key == ord("q"):
        break


video.release()
