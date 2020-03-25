#grayscale
import numpy as np
import cv2

import imutils
from imutils import contours





def get_contour_precedence(contour, cols):
    origin = cv2.boundingRect(contour)
    return origin[1] * cols + origin[0]

image = cv2.imread('out_test.png')

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
# cv2.imshow('gray',gray)
# cv2.waitKey(0)

#binary
ret,thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY_INV)
# cv2.imshow('second',thresh)
# cv2.waitKey(0)


#dilation
kernel = np.ones((5, 100), np.uint8)


img_dilation = cv2.dilate(thresh, kernel, iterations=5)
# cv2.imshow('dilated',img_dilation)
# cv2.waitKey(0)

#find contours im2
ctrs, hier = cv2.findContours(img_dilation.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)



#sort contours
# sorted_ctrs = sorted(ctrs, key=lambda ctr:get_contour_precedence(ctr, img_dilation.shape[1]))
for ctr in ctrs :
	x, y, w, h = cv2.boundingRect(ctr)
	print(str(x) + ' ' + str(y) + " " + str(w) + " " + str(h) + '\n')
	# print(str(cv2.boundingRect(ctr)[0]) + " " + str(cv2.boundingRect(ctr)[1]))



sorted_ctrs = sorted(ctrs, key=lambda ctr: get_contour_precedence(ctr, img_dilation.shape[1]))

# sorted_ctrs = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0] + cv2.boundingRect(ctr)[1] * image.shape[1] )


for i, ctr in enumerate(sorted_ctrs):
    # Get bounding box
    x, y, w, h = cv2.boundingRect(ctr)

    # Getting ROI
    roi = image[y:y+h, x:x+w]

    # show ROI
    #print('segment no:' + str(i))
    # cv2.imshow('segment no:'+str(i),roi)
    string = '/Users/anagh/Desktop/out/'
    string+= str(i)
    string += '.png'
    cv2.imwrite(string, roi)
    cv2.rectangle( image,(x,y),( x + w, y + h ),(90,0,255),2)
    # cv2.waitKey(0)

cv2.imshow('marked areas',image)
cv2.waitKey(0)



# !/usr/bin/python3
# 2018.01.16 01:11:49 CST
# 2018.01.16 01:55:01 CST
