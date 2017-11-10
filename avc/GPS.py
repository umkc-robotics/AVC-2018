import pynmea2
from serial import Serial, SerialException
from multiprocessing.managers import BaseManager
from multiprocessing import Process, Pipe
from collections import namedtuple
from threading import Event, Thread
from SerialHelper import wait_for_serial_connection
import sys
# set up Coordinate class -> named tuple
Coordinate = namedtuple("Coordinate", ["Latitude","Longitude","Timestamp"])
# set up a multiprocessing manager
class GPS_Manager(BaseManager):
	pass

GPS_Manager.register('Coordinate',Coordinate)
# done setting up a multiprocessing manager

# exception type for GPS class
class GPS_Exception(Exception):
	pass


class ThreadDriver(Thread):

	def __init__(self):
		self.keep_running = True
		self.raised_exception = "nothing"
		Thread.__init__(self)

	def run(self):
		"""
		Code that runs when thread instance gets started using .start()
		Returns: None
		"""
		try:
			raise Exception("ayylmao")
		except Exception as e:
			self.raised_exception = e

	def stop(self):
		"""
		Terminates thread cleanly
		Returns: None
		"""
		self.keep_running = False

class ProcessDriver(ThreadDriver):

	def __init__(self):
		# Process Pipe
		self.output_pipe, self.input_pipe = Pipe()
		# Decide whether or not process should be running
		self.keep_running = True
		ThreadDriver.__init__(self)

	def run(self):
		run_process()
		while self.keep_running:
			pass
		# put code here to properly terminate process

	def run_process(self):
		pass


class GPS(object):

	def __init__(self,conf):
		self.conf = conf
		self.current_coordinate = None
		self.fix_found = False
		self.should_stop = False
		# initialize and start a GPS_manager to share objects
		self.manager = GPS_Manager()
		self.manager.start()
		self.serial_process = None

	def run_gps_process(self):
		gps_proc = GPS_Process(self)
		gps_proc.run()

	def start(self):
		"""
		Attempts to connect to GPS via serial, starts a listener process
		Returns: None
		Raises: GPS_Exception when cannot connect to port (not connected?)
		"""
		try:
			serial_conn = Serial(self.conf["gps"]["port"],self.conf["gps"]["baud"])
		except SerialException as exception:
			raise GPS_Exception(exception)
		# wait for successful serial connection
		# start process
		self.should_stop = False
		self.current_coordinate = self.manager.Coordinate(None,None,None)
		self.serial_process = Process(target=self.run_gps_process,args=())
		#self.serial_process.daemon = True
		self.serial_process.start()

	def stop(self):
		self.should_stop = True

	def get_current_location(self):
		"""
		Returns Coordinate named tuple with current location
		Returns: Coordinage named tuple
		Raises: GPS_Exception when there is no fix on GPS
		"""
		return self.current_coordinate
		# get latest GPS location, as set by GPS child process

	def has_fix(self):
		"""
		Getter for whether or not GPS is fixed and providing real data
		Returns: True/False depending on if GPS has gotten a fix
		"""
		return self.fix_found == True


class GPS_Process:

	def __init__(self, driver):
		self.driver = driver

	def run(self):
		while not (self.driver.should_stop):
			print "reading line..."
			data = self.driver.serial_conn.readline()
			# check to see if line is type GGA
			if data[0:6] == '$GPGGA':
				print data
				parsed_data = pynmea2.parse(data)
				if parsed_data.latitude != 0:
					self.driver.fixed_event = True
				else:
					self.driver.fixed_event = False
				print parsed_data.latitude

				self.driver.coordinate_object.Latitude = parsed_data.latitude
				self.driver.coordinate_object.Longitude = parsed_data.longitude
				self.driver.coordinate_object.Timestamp = parsed_data.timestamp
				
				#print coordinate_object


#def gps_process(driver):
#	"""
#	Function that will format data from gps serial obj and save it in coordinate_object
#	The fixed event will be set when there is a fix, and cleared when there is none
#	"""
#	print "ayylmao"
#	#raise GPS_Exception("process error")
#	try:
#		driver.serial_conn = Serial(conf["gps"]["port"],conf["gps"]["baud"])
#	except SerialException as exception:
#		raise GPS_Exception(exception)
#	while not (should_stop):
#		print "reading line..."
#		data = driver.serial_conn.readline()
#		# check to see if line is type GGA
#		if data[0:6] == '$GPGGA':
#			print data
#			parsed_data = pynmea2.parse(data)
#			if parsed_data.latitude != 0:
#				fixed_event = True
#			else:
#				fixed_event = False
#			print parsed_data.latitude
#
#			driver.coordinate_object.Latitude = parsed_data.latitude
#			driver.coordinate_object.Longitude = parsed_data.longitude
#			driber.coordinate_object.Timestamp = parsed_data.timestamp
#			
#			print coordinate_object


