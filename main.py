# Importing
import numpy as np
import cv2


def go():
    print("Go")


def stop():
    print("Stop")


# Capturing Video
cap = cv2.VideoCapture(0)

while True:
    _, img = cap.read()
    # Converting RGB to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # defining the range of red color
    red_lower = np.array([136, 87, 111], np.uint8)
    red_upper = np.array([180, 255, 255], np.uint8)

    # defining the Range of green color
    green_lower = np.array([65, 60, 60], np.uint8)
    green_upper = np.array([80, 255, 255], np.uint8)

    # finding the range of red and green color in the image
    red = cv2.inRange(hsv, red_lower, red_upper)
    green = cv2.inRange(hsv, green_lower, green_upper)

    # Morphological transformation, Dilation
    kernal = np.ones((5, 5), np.int8)

    red = cv2.dilate(red, kernal)
    resr = cv2.bitwise_and(img, img, mask=red)

    green = cv2.dilate(green, kernal)
    resg = cv2.bitwise_and(img, img, mask=green)

    # Tracking the Red Color
    contours, hierarchy = cv2.findContours(red, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(img, "Red Color", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255))
            stop()

    # Tracking the green color
    contours, hierarchy = cv2.findContours(green, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for pic, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 300:
            x, y, w, h = cv2.boundingRect(contour)
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(img, "Green Color", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0))
            go()
    cv2.imshow("Traffic Control", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
