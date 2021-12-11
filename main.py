import cv2 as cv
import sys

img = cv.imread("test.jpg")

if img is None:
    sys.exit("Kuvan lukeminen ei onnistunut")

cv.imshow("Kuva", img)
key = cv.waitKey(0)

if key == ord("s"):
    cv.imwrite("starry_night.png", img)