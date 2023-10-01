import cv2
import time
import glob
from emailing import send_email

# we create a script that runs the webcam and pressing "q" will stop it

video = cv2.VideoCapture(0)
time.sleep(1)

first_frame = None
status_list = []
count = 1

while True:
    status = 0
    check1, frame = video.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # converting to grayscale pixels
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    if first_frame is None:
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # if a pixel is greater than 60 it will be set to 255,
    # for threshold if we use black and white
    # we use [1] as an index to get the 2nd item
    # inscrease the value (exp 60) to have only white pixels for the dynamic value
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    # dilate is to process the frame
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow("My video", dil_frame)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # if contour is too small it will be ignored
        if cv2.contourArea(contour) < 10000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        if rectangle.any():
            status = 1
            # store img
            cv2.imwrite(f"images/{count}.png", frame)
            count += 1
            # we produce a list of images
            all_images = glob.glob("images/*.png")
            # we prepare only one image from the list using an int
            index = int(len(all_images) / 2)
            image_object = all_images[index]
            send_email()

    status_list.append(status)
    # we extract only the last 2 items from the list
    status_list = status_list[-2:]
    # if detected object exits the frame
    if status_list[0] == 1 and status_list[1] == 0:
        send_email()
    print(status_list)

    cv2.imshow("Video", frame)
    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
