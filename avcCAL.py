from datetime import datetime
from time import sleep
import os
import numpy as np
#import matplotlib.pyplot as plt
import cv2
import math

location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
print location
saveLoc = location + '/cal_pictures'
if not os.path.exists(saveLoc): os.makedirs(saveLoc)

cap = cv2.VideoCapture(0)

scale = 0.75
#MARKER INFO
#markerLower = (97,35,35) #marker color is blue
#markerUpper = (110,255,255)
#markerLower = (23,70,70) #marker color is yellow
#markerUpper = (50,255,255)
markerLower = (35,35,35) #marker color is green
markerUpper = (87,255,255)
markerDraw = (0,0,255)
marker = (markerLower,markerUpper,markerDraw,"marker")
markerDrawBottom = (255,0,0)
#COMBINE
colors_track = [marker]

#mode toggles:
#first is marker calibration
#second is distance calibration
modes = [False,False,False,False]

xd = 0
yd = 0
print_distance = False
x_mouse = 0
y_mouse = 0
print_hsv = False
default_hsv = (55,25,255)
hsv_color = default_hsv
mark_step = 0
undistort = False
can_undistort = False
camera_matrix = [[-1,0,-1],[0,-1,-1],[0,0,1]]
distortion_coeff = [-99,-99,-99,-99,-99]
flip = False

if not os.path.exists(saveLoc+'/calvalues.txt'):
	with open(saveLoc+'/calvalues.txt', "a") as makeprot:
		makeprot.write("")

font = cv2.FONT_HERSHEY_SIMPLEX


def import_camcal():
	try:
		with open(saveLoc+'/camvalues.txt',"r") as camval:
			cam_mat_line = camval.readline().strip().split(',')
			dist_coeff_line = camval.readline().strip().split(',')
			if len(cam_mat_line) != 4 or len(dist_coeff_line) != 5:
				print("Cam Cal Values Error: not enough values read in")
				return False
			#insert values into cam matrix
			camera_matrix[0][0] = float(cam_mat_line[0])
			camera_matrix[0][2] = float(cam_mat_line[1])
			camera_matrix[1][1] = float(cam_mat_line[2])
			camera_matrix[1][2] = float(cam_mat_line[3])
			#insert values into distort coeffs
			for i in range(0,5):
				distortion_coeff[i] = float(dist_coeff_line[i])
			#check for proper import
			for i in range(0,3):
				for j in range(0,3):
					if camera_matrix[i][j] == -1:
						print "a value at %s,%s has not been changed in cam matrix" % (str(i),str(j))
						return False
			for i in range(0,5):
				if distortion_coeff[i] == -99:
					print "a value at %s has not been changed in distort coeffs" % str(i)
					return False
			return True

	except:
		return False	

if (import_camcal() == False):
	print "cam import values not found, will not undistort"
else:
	undistort = True
	can_undistort = True
	camera_matrix = np.array(camera_matrix)
	distortion_coeff = np.array(distortion_coeff)

def on_mouse(event,x,y,flag,param):
	global x_mouse,y_mouse,print_hsv,print_distance,modes
	if(event==cv2.EVENT_MOUSEMOVE):
		x_mouse = x
		y_mouse = y
	if(event==cv2.EVENT_LBUTTONDOWN):
		print_hsv = True
		if modes[2]:
			print_distance = True

def show_HSV_mouse(frame):
	global x_mouse,y_mouse,print_hsv,hsv_color,modes,font
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	cv2.setMouseCallback("Frame",on_mouse,0)
	s = hsv[y_mouse,x_mouse]
	if not modes[2]:
		cv2.putText(frame,str(s[0])+","+str(s[1])+","+str(s[2]),(x_mouse,y_mouse),font,0.6,hsv_color,2)
		cv2.putText(frame,str(x_mouse)+","+str(y_mouse),(x_mouse,y_mouse+23),font,0.6,hsv_color,2)
	else:
		frameh,framew = frame.shape[:2]
		point_1 = (x_mouse,y_mouse)
		point_2 = (framew/2,frameh)
		cv2.circle(frame, point_1, 5, markerDrawBottom, -1)
		cv2.circle(frame, point_2, 5, markerDrawBottom, -1)
		cv2.line(frame,point_1,point_2,(255,0,255),2)



	if print_hsv:
		print "At (%s,%s): %s,%s,%s" % (x_mouse,y_mouse,s[0],s[1],s[2])
		print_hsv = False
		return (s,(x_mouse,y_mouse))
	return None

def getYtoDistCoeff(p_u,p_y):
	#return np.polyfit(p_y,p_u,2)
	return np.polyfit(p_y,p_u,3)

def getYtoXCoeff(p_x,p_y):
	return np.polyfit(p_y,p_x,1)

def YtoX(y,ydim,coeff):
	#y = ydim-y
	return ((coeff[0]*y)+coeff[1])

def yDist(y,ydim,coeff):
	y = ydim-y
	#return ((coeff[0]*(y**2))+(coeff[1]*y)+coeff[2])
	return ((coeff[0]*(y**3))+(coeff[1]*(y**2))+(coeff[2]*y)+coeff[3])

def xDist(x,y,xdim,ydim,coeff):
	y = ydim-y
	return float((abs(x)-(xdim/2)))/YtoX(y,ydim,coeff)

def calcAngleDev(x,y,xdim,ydim,coeffQuad,coeffLin):
	global print_distance
	yd = abs(yDist(y,ydim,coeffQuad))
	xd = xDist(x,y,xdim,ydim,coeffLin)
	if print_distance:
		print "yd:" + str(yd)
		print "xd:" + str(xd)
		print_distance = False
	return math.degrees(math.atan(xd/yd))

def displayAngle(frame,coeffQuad,coeffLin):
	global hsv_color,font
	ydim,xdim = frame.shape[:2]
	angle = calcAngleDev(x_mouse,y_mouse,xdim,ydim,coeffQuad,coeffLin)
	cv2.putText(frame,str(angle),(xdim/2,ydim-30),font,0.6,hsv_color,2)

def track():
	global flip,camera_matrix,distortion_coeff,undistort,modes,colors_track,mark_step,hsv_color,marker,default_hsv,x_mouse,y_mouse,scale
	previous_color = marker

	cal_step = 0
	points_units = []
	points_y = []
	points_x = []
	#coefficientsYtoDist = [0,0,0]
	coefficientsYtoDist = [0,0,0,0]
	coefficientsYtoX = [0,0]


	while(1):
		ret,frame = cap.read()

		frame = cv2.resize(frame, (0,0), fx = scale, fy = scale) #change size of frame to process
		if (flip):
			frame = cv2.flip(frame,-1)
		if (undistort):
			h,w = frame.shape[:2]
			newcameramtx, roi = cv2.getOptimalNewCameraMatrix(camera_matrix, distortion_coeff, (w, h), 0, (w, h))
			frame = cv2.undistort(frame, camera_matrix, distortion_coeff, None, newcameramtx)
		blurred = cv2.GaussianBlur(frame, (11, 11), 0)
		hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
		pixel = show_HSV_mouse(frame)

		for color in colors_track:
			if color[0] != previous_color[0]:
				print str(color[0])
				print str(color[1])
				previous_color = color
			mask = cv2.inRange(hsv, color[0], color[1])
			mask = cv2.erode(mask, None, iterations=2)
			mask = cv2.dilate(mask, None, iterations=2)

			cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)[-2]
			center = None
			if modes[3]:
				if len(cnts) > 0:
					c = max(cnts, key=cv2.contourArea)
					area = cv2.contourArea(c)
					if area > 1000:
						M = cv2.moments(c)
						center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
						cv2.circle(frame, center, 5, color[2], -1) #dot color
						x,y,w,h = cv2.boundingRect(c)
						cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
						#print color[3] + ": %s,%s" % (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
						cv2.circle(frame, (center[0],y+h) , 5, markerDrawBottom, -1)
						#print ""

			cv2.imshow(color[3], mask) #window name

		frameh,framew = frame.shape[:2]
		cv2.line(frame,(framew/2,frameh),(framew/2,0),(255,255,0))

		if modes[2]:
			displayAngle(frame,coefficientsYtoDist,coefficientsYtoX)

		cv2.imshow("Frame", frame)

		if modes[0]:
			#print "Choose LOWER BOUND (CLICK PIXEL TO CHOOSE):"
			if pixel != None:
				if mark_step == 0:
					markerLowerN = (int(pixel[0][0])-5,30,30)
					#markerLowerN = (int(pixel[0][0]),int(pixel[0][1]),int(pixel[0][2]))
					hsv_color = (0,255,255)
					mark_step += 1
				elif mark_step == 1:
					markerUpperN = (int(pixel[0][0])+5,255,255)
					#markerUpperN = (int(pixel[0][0]),int(pixel[0][1]),int(pixel[0][2]))
					colors_track[0] = (markerLowerN,markerUpperN,(0,0,255),"marker")
					hsv_color = default_hsv
					modes[0] = False
					mark_step = 0
					print "MARKER CALIBRATION COMPLETE"

		if modes[1]:
			if pixel != None:
				unit = 0
				points_x.append(abs(int(pixel[1][0])-(framew/2)))
				if cal_step != 0:
					if cal_step > 4:
						unit = cal_step-2
					elif cal_step == 1:
						unit = 0.5
					elif cal_step == 2:
						unit = 1.0
					elif cal_step == 3:
						unit = 1.5
					elif cal_step == 4:
						unit = 2.0
					points_units.append(unit)
					points_y.append(frameh-int(pixel[1][1]))

				else:
					unit = 0
					points_units.append(0)
					points_y.append(0)
				print "Saved: Point %s, Unit = %s, Y = %s, X = %s" % (cal_step,unit,points_y[cal_step],points_x[cal_step])
				cal_step += 1
				



		#x,y,w,h = cv2.boundingRect(cnt)
		#img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

		#####64-bit compatible
		key = cv2.waitKey(1) & 0xFF

		if key == ord('q'):
			break

		if key == ord('m'):
			if modes[0]: 
				modes[0] = False
				print "MARKER CALIBRATION DEACTIVATED"
				hsv_color = default_hsv
			else: 
				modes[0] = True
				mark_step = 0
				print "MARKER CALIBRATION ACTIVATED"
				hsv_color = (255,255,0)

		if key == ord('c'):
			if modes[1]:
				modes[1] = False
				print "PLANE CALIBRATION CANCELLED"
				hsv_color = default_hsv
			else:
				modes[1] = True
				modes[0] = False
				modes[2] = False
				cal_step = 0
				print "PLANE CALIBRATION STARTED"
				cal_step = 0
				points_units = []
				points_y = []
				points_x = []
				coefficientsYtoDist = [0,0,0,0]
				coefficientsYtoX = [0,0]
				hsv_color = (255,0,255)
				print "Line up cyan line on a grid vertical grid line."
				print "Select the point corresponding to the lowest horizontal "
				print "grid line and the closest vertical line to the right of the center."
				print "Unit: %s" % cal_step


		if key == ord('u'):
			if can_undistort:
				if undistort:
					undistort = False
				else:
					undistort = True
				print "undistorted (fixed)? %s" % undistort

		if key == ord('x'):
			if modes[1]:
				modes[1] = False
				hsv_color = default_hsv
				coefficientsYtoDist = getYtoDistCoeff(points_units,points_y)
				coefficientsYtoX = getYtoXCoeff(points_x,points_y)
				print str(coefficientsYtoDist)
				print str(coefficientsYtoX)
				with open(saveLoc+'/calvalues.txt', "wb") as calval:
					for coeff in coefficientsYtoDist:
						calval.write(str(coeff) + ",")
					calval.write(str(coefficientsYtoX[0])+","+str(coefficientsYtoX[1]))

				print "PLANE CALIBRATION COMPLETE"

		if key == ord('d'):
			if modes[2]:
				modes[2] = False
				print "Distance calculations turned off"
			else:
				if coefficientsYtoX[0] == 0 and coefficientsYtoX[1] == 0:
					print "Cannot start distance calculations; no calibration present"
				else:
					modes[2] = True
					print "Distance calculations turned on"

		if key == ord('l'):
			with open(saveLoc+'/calvalues.txt', "rb") as calval:
				line = calval.readline().strip()
				if line != "":
					values = line.split(',')
					try:
						coeffam = 4
						for n in range(0,coeffam):
							coefficientsYtoDist[n] = float(values[n])
						for n in range(0,2):
							coefficientsYtoX[n] = float(values[n+coeffam])
					except Exception,e:
						print "Error: %s" % str(e)
					else:
						print "Calibration values imported successfully!"
				else:
					"Error: Calibration file is empty!"


		if key == ord('1'):
			if modes[3]:
				modes[3] = False
				print "Marker NOT displayed"
			else:
				modes[3] = True
				print "Marker displayed"


		if key == ord('s'):
			now = datetime.now()
			timest = now.strftime("%Y%m%d%H%M%S")
			name = saveLoc + '/' + timest + '.png'
			print name
			cv2.imwrite(name, frame)
			print('picture taken')

		if key == ord('f'):
			flip = not flip;
			print "flipped: %s" % str(flip)


track()
cap.release()
cv2.destroyAllWindows()







