#grayscale
import numpy as np
import cv2

import imutils
from imutils import contours

import sys 
import subprocess
import os
from pathlib import Path 

filename_input = sys.argv[1]

def erode_image(filename):
    
    img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)

    # increase contrast
    pxmin = np.min(img)
    pxmax = np.max(img)
    imgContrast = (img - pxmin) / (pxmax - pxmin) * 255

    # increase line width
    kernel = np.ones((4, 4), np.uint8)
    imgMorph = cv2.erode(imgContrast, kernel, iterations = 2)

    # write
    cv2.imwrite(filename, imgMorph)



def get_contour_precedence(contour, cols):
    origin = cv2.boundingRect(contour)
    return origin[1] * cols + origin[0]




image = cv2.imread(filename_input)

# image = cv2.imread(filename)


gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# cv2.imshow('gray',gray)
# cv2.waitKey(0)

#binary
ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)


#dilation
kernel = np.ones((5, 100), np.uint8)


img_dilation = cv2.dilate(thresh, kernel, iterations=5)


#find contours im2
ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)



#sort contours
# sorted_ctrs = sorted(ctrs, key=lambda ctr:get_contour_precedence(ctr, img_dilation.shape[1]))
for ctr in ctrs :
	x, y, w, h = cv2.boundingRect(ctr)


sorted_ctrs = sorted(ctrs, key=lambda ctr: get_contour_precedence(ctr, img_dilation.shape[1]))

# sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * image.shape[1] )
path = os.path.abspath(os.getcwd()) + '/out_test/'
if(os.path.exists(path)):

    for f in Path(path).glob('*.png'):
        f.unlink()


for i, ctr in enumerate(sorted_ctrs):
    # Get bounding box

    x, y, w, h = cv2.boundingRect(ctr)

    # Getting ROI
    roi = image[y:y+h, x:x+w]

    # show ROI
    #print('segment no:' + str(i))
    # cv2.imshow('segment no:'+str(i),roi)
    string = 'out_test/'

    string+= str(i)
    string += '.png'
    # initial_directory = os.path.abspath(os.getcwd())

    cv2.imwrite(string, roi)
    # erode_image(string)
    # cv2.imshow(roi)
    cv2.rectangle( image,(x,y),( x + w, y + h ),(90,0,255),2)
    # cv2.waitKey(0)



# pipe = subprocess.check_call(["python", filename])

print("Splitting into lines is over")

