import cv2
import numpy as np
import glob
import os
import sys
current_path = os.getcwd()
sys.path.insert(0, current_path + '/Image_Calibration/')

dir_path = current_path + '/Image_Calibration/'

os.chdir(dir_path)

image = cv2.imread('46_image_set/raw_image_0_ff.png')

# initial values
fx, fy, cx, cy, k1, k2, p1, p2, k3 = 500, 500, 320, 240, 0.1, 0.1, 0.1, 0.1, 0.1

def update_values(x):
    global fx, fy, cx, cy, k1, k2, p1, p2, k3
    fx = cv2.getTrackbarPos('fx', 'Controls')
    fy = cv2.getTrackbarPos('fy', 'Controls')
    cx = cv2.getTrackbarPos('cx', 'Controls')
    cy = cv2.getTrackbarPos('cy', 'Controls')
    k1 = cv2.getTrackbarPos('k1', 'Controls') / 100.0
    k2 = cv2.getTrackbarPos('k2', 'Controls') / 100.0
    p1 = cv2.getTrackbarPos('p1', 'Controls') / 100.0
    p2 = cv2.getTrackbarPos('p2', 'Controls') / 100.0
    k3 = cv2.getTrackbarPos('k3', 'Controls') / 100.0

cv2.namedWindow('Controls')
cv2.resizeWindow('Controls', 400, 600)  # window size

cv2.createTrackbar('fx', 'Controls', 90, 2000, update_values)
cv2.createTrackbar('fy', 'Controls', -100, 1000, update_values)
cv2.createTrackbar('cx', 'Controls', -10000, 1000, update_values)
cv2.createTrackbar('cy', 'Controls', -10000, 1000, update_values)
cv2.createTrackbar('k1', 'Controls', -int(k1 * 100), 100, update_values)
cv2.createTrackbar('k2', 'Controls', -int(k2 * 100), 100, update_values)
cv2.createTrackbar('p1', 'Controls', -int(p1 * 100), 100, update_values)
cv2.createTrackbar('p2', 'Controls', -int(p2 * 100), 100, update_values)
cv2.createTrackbar('k3', 'Controls', -int(k3 * 100), 100, update_values)

while True:
    # set matrix
    camera_matrix = np.array([[fx, 0, cx], [0, fy, cy], [0, 0, 1]])
    dist_coeffs = np.array([k1, k2, p1, p2, k3])
    K=np.array([[93.16858864610276, 0.0, 150.8535602775792], [0.0, 91.92373264897513, 146.22342371914382],[0.0, 0.0, 1.0]])
    D=np.array([[0.14136243954038377], [0.29925561973923737], [-0.321789761587799],[0.11936916962615352]])

    # undistort
    undistorted_image = cv2.undistort(image, camera_matrix, dist_coeffs)

    cv2.imshow('Original Image', image)
    cv2.imshow('Undistorted Image', undistorted_image)

    if cv2.waitKey(1) & 0xFF == 27:  # 'Esc' quit
        break

cv2.destroyAllWindows()
