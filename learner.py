import cv2
import numpy as np
import time

cap = cv2.VideoCapture(0)
stamp = time.time()
while (True):
	_, frame = cap.read()
	
	cv2.imshow('This!',frame)
	dt = time.time() - stamp
	if (dt > 5):
		cap.release()
		cap = cv2.VideoCapture(0)
		cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,1280)
		cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,960)
		time.sleep(2)
		_, frame = cap.read()
		
		cv2.imwrite ('learner.jpg',frame)
		break
	
	k = cv2.waitKey(5) & 0xFF	
	if k == 27:
		
		break

# Aftermath 
cap.release()
cv2.destroyAllWindows()
