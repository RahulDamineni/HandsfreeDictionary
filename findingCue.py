# Version #1, Color processing successful.
# Cue found, results in 'mask'

#hsv = {(7,187,180);(13,133,123)}

import cv2
import numpy as np
import time
# Start Recording 
cap = cv2.VideoCapture(0)

# Calibrate.py results here to detect that orange thingy...
h,s,v,counter = 13,133,123,1

# Masking...
lower_colour = np.array([h,s,v])
upper_colour = np.array([180,255,255])

# declarations
centroid_x,centroid_y = 0,0
while(True) :
	
	_, frame = cap.read()
	
	# TO HSV
	hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	
	# Appying mask to extract output
	mask = cv2.inRange(hsv,lower_colour, upper_colour)
	
	# Displaying obtained mask. Uncomment below line to see the Joker's mask! :) 
	#cv2.imshow('Mask',mask)
	
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
	M = cv2.moments(contour_max)
	past_x,past_y = centroid_x,centroid_y
	centroid_x = int(M['m10']/M['m00'])
	centroid_y = int(M['m01']/M['m00'])
	dX,dY = (past_x-centroid_x),(past_y-centroid_y)
	print "dX, dY = ",dX,dY
	if (dX < 0):
		dX = -dX
	if (dY < 0):
		dY = -dY
	cv2.circle(mask,(centroid_x,centroid_y),10,(255,255,255),-1)
	
	
	# HERE COMES THE MUCH AWAITED CENTROID #
	print (centroid_x,centroid_y)
	
	cv2.imshow('Mask',mask)

	# Exit path here ....
	
	if ((dX < 5) or (dY < 5)):
		if (counter == 1):
			print "timer started ... "
			stamp =time.time()
			counter = 10
		
		dt = (time.time() - stamp)
		if (dt > 4) :
			
			cv2.imwrite('source.jpg',frame)
			print dt,stamp
			break
	elif ((dX > 5) or (dY > 5)):
		counter = 1
		print "timer RESET ... "
		
	k = cv2.waitKey(5) & 0xFF	
	if k == 27:
		
		break

# Aftermath 
cap.release()
cv2.destroyAllWindows()

