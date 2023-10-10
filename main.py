import cv2
import time
import glob
import os
from emailing import send_email  # custom module for sending emails
from threading import Thread

# We create a script that runs the webcam and pressing "q" will stop it


# Open the webcam
video = cv2.VideoCapture(0)
time.sleep(1)  # wait for the camera to initialize

# Initialize variables and lists
first_frame = None
status_list = []
count = 1


# Function to clean the image directory
def clean_folder(images):
    print(f"Cleaning the {images} directory...")
    images = glob.glob(f"{images}/*.png")
    for image in images:
        os.remove(image)
    print(f"{images} directory cleaned")


# Main loop to process the webcam feed
while True:
    status = 0
    check1, frame = video.read()  # read a frame from the video

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # convert frame to grayscale
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)  # apply gaussian blur

    if first_frame is None:
        first_frame = gray_frame_gau

    # Calculate the absolute difference between frames
    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # if a pixel is greater than 60 it will be set to 255,
    # for threshold if we use black and white
    # we use [1] as an index to get the 2nd item
    # increase the value (exp 60) to have only white pixels for the dynamic value

    # Thresholding to identify motion
    thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
    # dilate is to process the frame
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

    # Display the video feed and processed frame
    cv2.imshow("My video", dil_frame)

    # Find contours to detect motion
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

    status_list.append(status)
    # we extract only the last 2 items from the list
    status_list = status_list[-2:]
    # if detected object exits the frame
    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send_email, args=(image_object,))  # added a comma to make it a tuple
        email_thread.daemon = True
        clean_thread = Thread(target=clean_folder)
        clean_thread.daemon = True

        # Start threads for sending email and cleaning folder
        email_thread.start()
        clean_thread.start()

    print(status_list)

    # Display the video frame
    cv2.imshow("Video", frame)

    # Check for 'q' key press to exit loop
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

# Release the video
video.release()

# Clean the image directory
clean_folder("images")
