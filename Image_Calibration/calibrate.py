import numpy as np
import cv2
import pickle
import glob

CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720

chessboardSize = (10, 7)
frameSize = (CAMERA_WIDTH, CAMERA_HEIGHT)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chessboardSize[0], 0:chessboardSize[1]].T.reshape(-1, 2)

size_of_chessboard_squares_mm = 20
objp = objp * size_of_chessboard_squares_mm

objpoints = []
imgpoints = []

cap = cv2.VideoCapture(0)  # 0 corresponds to the default camera

while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ret, corners = cv2.findChessboardCorners(gray, chessboardSize, None)

    if ret:
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        objpoints.append(objp)
        imgpoints.append(corners)

        cv2.drawChessboardCorners(frame, chessboardSize, corners2, ret)
        cv2.imshow('Webcam Calibration', frame)

    key = cv2.waitKey(1)
    if key == 27:  # Press 'Esc' to exit
        break
    elif key == 32:  # Press 'Space' to capture and calibrate
        ret, cameraMatrix, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, frameSize, None, None)
        print("Calibration successful!")
        break

cap.release()
cv2.destroyAllWindows()

# Save the camera calibration result for later use
pickle.dump((cameraMatrix, dist), open("calibration.pkl", "wb"))
pickle.dump(cameraMatrix, open("cameraMatrix.pkl", "wb"))
pickle.dump(dist, open("dist.pkl", "wb"))