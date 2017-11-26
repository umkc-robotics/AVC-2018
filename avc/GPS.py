import pynmea2
from serial import Serial, SerialException
from time import sleep
from math import atan2, degrees, sqrt
from AsyncDriver import ThreadDriver, ProcessDriver

# set up Coordinate class 
class Coordinate(object):

	def __init__(self, latitude, longitude, timestamp=None):
		self.latitude = latitude
		self.longitude = longitude
		self.timestamp = timestamp

	def __str__(self):
		return "{},{},{}".format(self.latitude,self.longitude,self.timestamp)



class GPS_Exception(Exception):
	pass



class GPS(ProcessDriver):

	def __init__(self, conf):
		self.conf = conf
		self.current_coordinate = Coordinate(0,0,0)
		ProcessDriver.__init__(self, gps_process, (conf,))
		self.minimum_overlap = conf["gps"]["minimum_overlap"]
		self.daemon = conf["daemon"]

	def is_fixed(self):
		"""
		Returns boolean explaining whether or not gps has a fix
		"""
		if self.current_coordinate.latitude != 0 or self.current_coordinate.longitude != 0:
			return True
		else:
			return False 

	def is_overlapping(self, coordinate):
		"""
		Returns boolean corresponding to if provided coordinate overlaps current location
		"""
		distance = sqrt((coordinate.latitude-self.current_coordinate.latitude)**2 + (coordinate.longitude-self.current_coordinate.longitude)**2)
		return distance <= self.minimum_overlap

	def get_desired_heading(self, current_heading, goal_coordinate):
		"""
		Returns angle difference between current heading and direction towards goal
		"""
		desiredAbsoluteHeading = self.calculate_angle_to_node(goal_coordinate)
		desiredRelativeHeading = desiredAbsoluteHeading - current_heading
		# make sure the resulting angle is between -179.99... and 180 degrees
		if desiredRelativeHeading > 180:
			desiredRelativeHeading -= 360
		elif desiredRelativeHeading == -180:
			desiredRelativeHeading = abs(desiredRelativeHeading)
		elif desiredRelativeHeading < -180:
			desiredRelativeHeading += 360

		return desiredRelativeHeading

	def calculate_angle_to_node(self, desired):
		"""
		Angle obtained when desired coordinate is at following locations:
		            0
		            .
		           /|\
		            |
		            |
		            |
		-90 <-------X-------> 90
		            |
		            |
		            |
		           \|/
		            `
		           180
		In the South-West quadrant, angles are between -90 and -179.99...
		"""
		xDiff = desired.longitude - self.current_coordinate.longitude
		yDiff = desired.latitude - self.current_coordinate.latitude
		return degrees(atan2(yDiff,xDiff))


	def get_location(self):
		"""
		Returns a Coordinate object corresponding to current location
		"""
		return self.current_coordinate

	def handle_input(self, input_obj):
		# if input is a Coordinate object, set coordinate to that object
		if isinstance(input_obj, Coordinate):
			self.current_coordinate = input_obj
		else:
			print "RECEIVED WEIRD INPUT: {}".format(input_obj)



def gps_process(conf, comm_pipe):
	gps_serial = None
	print "GPS PROCESS STARTED"
	try:
		keep_running = True
		# start serial process, raise a GPS exception if fails
		try:
			gps_serial = Serial(conf["gps"]["port"],conf["gps"]["baud"])
		except SerialException as e:
			raise GPS_Exception(e)
		print "CONNECTED TO GPS"
		while keep_running:
			# check pipe for messages
			if comm_pipe.poll():
				received = comm_pipe.recv()
				if received == "EXIT":
					keep_running = False
					break
			# get serial input
			data = gps_serial.readline()
			# check to see if line is type GGA
			if data[0:6] == '$GPGGA':
				parsed_data = pynmea2.parse(data)
				current_coord = Coordinate(parsed_data.latitude,parsed_data.longitude,parsed_data.timestamp)
				# send coordinate through pipe
				comm_pipe.send(current_coord)

	except Exception as e:
		try:
			print "SENDING ERROR..."
			comm_pipe.send(e)
		except IOError as e:
			print "IO ERROR on GPS"
	finally:
		if isinstance(gps_serial,Serial):
			gps_serial.close()
