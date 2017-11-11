import pynmea2
from serial import Serial, SerialException
from collections import namedtuple
from SerialHelper import wait_for_serial_connection
from time import sleep
from AsyncDriver import ThreadDriver, ProcessDriver
# set up Coordinate class -> named tuple
Coordinate = namedtuple("Coordinate", ["Latitude","Longitude","Timestamp"])



class GPS_Exception(Exception):
	pass



class GPS(ProcessDriver):

	def __init__(self, conf):
		self.conf = conf
		self.current_coordinate = Coordinate(0,0,0)
		ProcessDriver.__init__(self, gps_process, (conf,))

	def is_fixed(self):
		if self.current_coordinate.Latitude != 0 or self.current_coordinate.Longitude != 0:
			return True
		else:
			return False 

	def get_location(self):
		"""
		Returns a Coordinate object corresponding to current location
		"""
		return self.current_coordinate

	def handle_input(self, input_obj):
		# if input is a Coordinate object, set coordinate to that object
		if isinstance(input_obj, Coordinate):
			self.current_coordinate = input_obj



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
		print "CONNECTED To GPS"
		while keep_running:
			# check pipe for messages
			if comm_pipe.poll():
				received = comm_pipe.recv()
				if received == "EXIT":
					keep_running = False
			# get serial input
			data = gps_serial.readline()
			# check to see if line is type GGA
			if data[0:6] == '$GPGGA':
				parsed_data = pynmea2.parse(data)
				current_coord = Coordinate(parsed_data.latitude,parsed_data.longitude,parsed_data.timestamp)
				# send coordinate through pipe
				comm_pipe.send(current_coord)

	except Exception as e:
		#try:
		print "SENDING ERROR..."
		comm_pipe.send(e)
		#except IOError as e:
		#	pass
	finally:
		if isinstance(gps_serial,Serial):
			gps_serial.close()
