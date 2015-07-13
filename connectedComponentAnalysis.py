# Version #2, Connected component analysis.
# previous version summary, Centroid of Cue : Found!
# This version output : Nearest connected component identified and segregated.

#hsv = {(7,187,180);(13,133,123)}

import cv2
import numpy as np
import math

# Start Recording 
cap = cv2.VideoCapture(0)

# Calibrate.py results here to detect that orange thingy...
h,s,v = 13,133,123

# Masking...
lower_colour = np.array([h,s,v])
upper_colour = np.array([180,255,255])

while(True) :
	
	_, frame = cap.read()
	
	# TO HSV
	hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	
	# Appying mask to extract output
	mask = cv2.inRange(hsv,lower_colour, upper_colour)
	
	# Displaying obtained mask. Uncomment below line to see the Joker's mask! :) 
	# cv2.imshow('Mask',mask)
	
	# Finding contours to find Moments & Centroid 
	contours, hierarchy = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	
	
	# Uncomment the below line to visualize contours ... 
	# cv2.drawContours(mask,contours,-1,(255,255,255),-1) 
	
	# Initializing area parameter and its corresponding contour, named 'contour_max'
	area_max = 0

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
	#	print (centroid_x,centroid_y)
#---------------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------------------------------#

	# Thresholding ... << Choose between Gaussian and Mean methods & don't forget Weighted sum subtraction >>
	binary = cv2.adaptiveThreshold(cv2.cvtColor(frame, cv2.cv.CV_BGR2GRAY), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 2) 
	cv2.imshow('Actual binary',binary)
	
	# Removing Salt & Pepper
	binary = cv2.medianBlur(binary,1)
	#cv2.imshow('Deblurred binary',binary)
	
	# Updating Kernel definitions ...
	kernel = np.ones((4,4),np.uint8)
	
	# Eroding ... << A lot of pepper noise in-here! Get rid if that. >>
	binary_eroded = cv2.erode(binary,kernel,iterations = 1)
	cv2.imshow('Eroded binary', binary_eroded)
	# Contours for word extraction. Real-Time approach. Gonna implement of frame-shoot approach on Galileo.
	contours, hierarchy = cv2.findContours(binary,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	print len(contours)
	
	cv2.imshow('Eroded binary Aftercontours', binary_eroded)
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
		
		if((len(cnt) != len(contour_max)) and (cv2.contourArea(cnt) > 1)):
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
	
	# Thus we have found the word's centroid! 		
	cv2.circle(mask,(centroid_x,centroid_y),10,(255,255,255),-1)
	cv2.circle(binary_eroded,(centroid_word_x,centroid_word_y),10,(255,255,255),-1)
	cv2.circle(frame,(centroid_word_x,centroid_word_y),10,(0,255,2),-1)
	cv2.circle(frame,(centroid_x,centroid_y),10,(255,0,255),-1)
	
	
	
	cv2.imshow('Mask with ORIGIN',mask)
	cv2.imshow('Eroded image with WORD Center Marked',binary_eroded)
	cv2.imshow('frame with WORD!', frame)

	# Exit path here ....
	k = cv2.waitKey(0) & 0xFF
	#if k == 27:
	#	cv2.imwrite('eroded.png',binary_eroded)
	#	break

# Aftermath 
cap.release()
cv2.destroyAllWindows()

