#proc_feed_v3.py
#Previous version summary : Area parameter successfully implemented 
import cv2
import numpy as np

cv2.namedWindow("Here you go!")
cv2.namedWindow("bin")
vc = cv2.VideoCapture(1)

if vc.isOpened(): 				#  To get the first frame
    rval, frame = vc.read()
    frame = cv2.imread('template.jpg')	
else:
    rval = False

while rval:
	
	frame_gray = cv2.cvtColor(frame,cv2.cv.CV_BGR2GRAY) # BGR2GRAY	
	thr = frame_gray.sum() / frame_gray.size  #thre				#DO  STUFF
    	retval,frame_bin  = cv2.threshold(frame_gray,100,255,cv2.THRESH_BINARY_INV)  #Gray2Binary
	frame_binp = np.array(frame_bin)
	contours,hierarchy = cv2.findContours(frame_bin,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE) #finding contours
	
	cv2.drawContours(frame_bin,contours,-1,255,-1)
	
	mask = np.zeros(frame_gray.shape,np.uint8)   
	for hierarchy,cnt in enumerate(contours):
		
		if cv2.contourArea(cnt) > 5000:
		    
		    cv2.drawContours(mask,[cnt],0,255,-1)
		    ellipse = cv2.fitEllipse(cnt)
		    c = ellipse[0]
		    cv2.circle(frame,(int(c[0]),int(c[1])),2,(0,255,0),3)
		    cv2.ellipse(mask,ellipse,255,3)
		    print ellipse[0]
	cv2.imshow("Here you go!", frame)
		    
	cv2.imshow("bin",mask)

	rval, frame = vc.read()
	key = cv2.waitKey(20)
	if key == 27: 
						# exit on ESC
		break
