
#hsv = {(7,187,180);(13,133,123)}

import cv2
import numpy as np
import math



# Calibrate.py results here to detect that orange thingy...
h,s,v = 13,133,123

# Masking...
lower_colour = np.array([h,s,v])
upper_colour = np.array([180,255,255])

# Finding centroid of the cue using Colour Image Processing...

# Input colour image
frame = cv2.imread('source.jpg',-1)
#cv2.imshow('Source',frame)

# TO HSV
hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

# Appying mask to extract output
mask = cv2.inRange(hsv,lower_colour, upper_colour)

# Displaying obtained mask. Uncomment below line to see the Joker's mask! :) 
#cv2.imshow('Mask',mask)

# Finding contours to find Moments & Centroid 
contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

# Init ...
area_max = 0

# Finding biggest among contours interms of area.
###### !!!!Computational Burden!!!! You'll improve this somehow. #######
for h,cnt in enumerate(contours):
	# Finding area of each contour and picking up the onw with max area. 
	area = cv2.contourArea(cnt)
	if (area > area_max) :
		area_max = area
		contour_max = cnt
		
# Finding centroid of that cue.
try :
	M = cv2.moments(contour_max)
	centroid_x = int(M['m10']/M['m00'])
	centroid_y = int(M['m01']/M['m00'])
except :
	print "Empty contour!"
	
# HERE COMES THE MUCH AWAITED CENTROID #
#print (centroid_x,centroid_y)

# Thresholding ... << Choose between Gaussian and Mean methods & don't forget Weighted sum subtraction >>
#binary = cv2.adaptiveThreshold(cv2.cvtColor(frame, cv2.cv.CV_BGR2GRAY), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 7) 
_,binary = cv2.threshold(cv2.cvtColor(frame, cv2.cv.CV_BGR2GRAY), 127,255,cv2.THRESH_BINARY) 

#cv2.imshow('Binary of Source',binary)

# Removing Salt & Pepper
# binary = cv2.medianBlur(binary,1)
# cv2.imshow('Deblurred binary',binary)

# Updating Kernel definitions ...
kernel = np.ones((6,6),np.uint8)

# Eroding ... << A lot of pepper noise in-here! Get rid if that. >>
binary_eroded = cv2.erode(binary,kernel,iterations = 1)
#cv2.imshow('Eroded binary', binary_eroded)

# Contours for word extraction. Real-Time approach. Gonna implement of frame-shoot approach on Galileo.
contours, hierarchy = cv2.findContours(binary_eroded,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
print len(contours)

# Uncomment the below line to visualize contours ... 
#cv2.drawContours(binary_eroded,contours,-1,(255,255,255),-1)
#cv2.imshow('Eroded binary Aftercontours', binary_eroded)

###### !!!!Computational Burden!!!! You'll improve this somehow. #######
for h,cnt in enumerate(contours):
	# Finding area of each contour and picking up the onw with max area. 
	area = cv2.contourArea(cnt)
	if (area > area_max) :
		area_max = area
		contour_max = cnt

# Another declaration! 
d_min,cent_x,cent_y,i = 10000000, 1000,1000,0

# Calculating centroids of all contours except the one with max area
for h,cnt in enumerate(contours):
# If this cnt is not max contour
	
	if((len(cnt) != len(contour_max)) and (cv2.contourArea(cnt) > 100)):
		# Then find its centroid
		M = cv2.moments(cnt)
		try:
			cent_x = int(M['m10']/M['m00'])
			cent_y = int(M['m01']/M['m00'])
		except :
			i = i+1
			print i
	# See how far it is from out origin .
			
		d = math.sqrt(((cent_y-centroid_y)*(cent_y-centroid_y)) + ((cent_x-centroid_x)*(cent_x-centroid_x)))
		# Is this the smallest distance we've found so far ?
		if (d < d_min):
			d_min = d
			centroid_word_x = cent_x
			centroid_word_y = cent_y
			print (cent_x,cent_y), "With separation, ", d
			wordContour = cnt
word = frame-frame
rect = cv2.minAreaRect(wordContour)
box = cv2.cv.BoxPoints(rect)
box = np.int0(box)
cv2.drawContours(word,[box],0,(255,255,255),-1)
#cv2.imshow('Word !',word)
(h,w) = frame.shape[:2]
M = cv2.getRotationMatrix2D(rect[0], rect[2], 1.0)
rotated = cv2.warpAffine(frame, M, (w, h))
rotatedMask = cv2.warpAffine(word, M, (w, h))
rotated_bro = cv2.bitwise_and(rotated,rotatedMask)
word = rotated_bro.copy()
_,binaryWord = cv2.threshold(cv2.cvtColor(rotated_bro, cv2.cv.CV_BGR2GRAY), 5,255,cv2.THRESH_BINARY)
contoursW, hierarchyW = cv2.findContours(binaryWord,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

rectW = cv2.minAreaRect(contoursW[0])
box = cv2.cv.BoxPoints(rectW)
box = np.int0(box)
print box

cv2.drawContours(binaryWord,[box],0,(255,255,255),-1)
cv2.imshow("rotated", rotated_bro)
a = box[1]
c = box[3]
print "a is ", a , "c is ", c
roi = rotated_bro[a[1]:c[1],a[0]:c[0]]

cv2.imshow('ROI',roi)
cv2.imwrite('word.png',roi)

# Thus we have found the word's centroid! 		
#cv2.circle(mask,(centroid_x,centroid_y),10,(255,255,255),-1)
#cv2.circle(binary_eroded,(centroid_word_x,centroid_word_y),10,(255,255,255),-1)
cv2.circle(frame,(centroid_word_x,centroid_word_y),10,(0,255,2),-1)
cv2.circle(frame,(centroid_x,centroid_y),10,(255,0,255),-1)
	
	
	
#cv2.imshow('Mask with ORIGIN',mask)
#cv2.imshow('Eroded image with WORD Center Marked',binary_eroded)
cv2.imshow('frame with WORD!', frame)

print h,"And",w
cv2.waitKey(0)
