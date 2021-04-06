import cv2
import numpy as np
import time

if False:
    foldername = "/fn"
    filename = foldername+"/ForestSmoke/video03.avi"
    cap = cv2.VideoCapture(filename)
else:
    cap = cv2.VideoCapture(1)


def nothing(x):
    pass


# Creating a window for later use
cv2.namedWindow('result')

# Starting with 100's to prevent error while masking
h, s, v = 100, 100, 100
h_l, s_l, v_l = 0, 0, 0


# Creating track bar
cv2.createTrackbar('h_l', 'result', 0, 179, nothing)
cv2.createTrackbar('s_l', 'result', 0, 255, nothing)
cv2.createTrackbar('v_l', 'result', 0, 255, nothing)
cv2.createTrackbar('h', 'result', 0, 179, nothing)
cv2.createTrackbar('s', 'result', 0, 255, nothing)
cv2.createTrackbar('v', 'result', 0, 255, nothing)

while(1):

    _, frame = cap.read()

    # converting to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('gray_scale', gray_scale)

    cv2.imshow('h', hsv[:, :, 0])
    cv2.imshow('s', hsv[:, :, 1])
    cv2.imshow('v', hsv[:, :, 2])

    # get info from track bar and appy to result
    h_l = cv2.getTrackbarPos('h_l', 'result')
    s_l = cv2.getTrackbarPos('s_l', 'result')
    v_l = cv2.getTrackbarPos('v_l', 'result')
    h = cv2.getTrackbarPos('h', 'result')
    s = cv2.getTrackbarPos('s', 'result')
    v = cv2.getTrackbarPos('v', 'result')

    # Normal masking algorithm
    lower_blue = np.array([h_l, s_l, v_l])
    upper_blue = np.array([h, s, v])

    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('result', result)

    key = cv2.waitKey(30) & 0xff
    if key == ord("q"):
        break

cap.release()

cv2.destroyAllWindows()
