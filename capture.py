import cv2
import imutils

cam = cv2.VideoCapture(0)


def get_frame(flipped=False):
    _, frame = cam.read()
    if flipped:
        return imutils.resize(cv2.rotate(frame, cv2.ROTATE_180))
    return frame


def toGreyScale(frame):
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return cv2.GaussianBlur(grey, (21, 21), 0)


def isOccupied(frame0, frame1):
    grey0 = toGreyScale(frame0)
    grey1 = toGreyScale(frame1)

    frameDelta = cv2.absdiff(grey0, grey1)
    thresh = cv2.threshold(frameDelta, thresh=30, maxval=255, type=cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=1)
    contours = cv2.findContours(
        thresh.copy(), mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_SIMPLE
    )
    contours = imutils.grab_contours(contours)
    for c in contours:
        if cv2.contourArea(c) > 2000:
            return True

    return False
