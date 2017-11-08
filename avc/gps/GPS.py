import pynmea2
import serial
from collections import namedtuple
from multiprocessing.managers import BaseManager
from threading import Event

# set up Coordinate class -> named tuple
Coordinate = namedtuple("Coordinate", ["Latitude","Longitude"])

# set up a multiprocessing manager
class GPS_Manager(BaseManager):
	pass

GPS_Manager.register('Coordinate',Coordinate)
# done setting up a multiprocessing manager

# exception type for GPS class
class GPS_Exception(Exception):
	pass


class GPS(object):

	def __init__(self,conf):
		self.conf = conf
		self.current_coordinate = None
		self.fix_found = Event()
		self.should_stop = Event()
		# initialize and start a GPS_manager to share objects
		self.manager = GPS_Manager()
		self.manager.start()
		# initialize a serial process

	def start(self):
		"""
		Attempts to connect to GPS via serial, starts a listener process
		Returns: None
		Raises: GPS_Exception when cannot connect to port (not connected?)
		"""
		return
		# use "gps_port" from config to create serial object
		# and then start a process to validate data and save it

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
		return self.fix_found.is_set()

def gps_process(serial_obj, coordinate_object, fixed_event, should_stop):
	"""
	Function that will format data from gps serial obj and save it in coordinate_object
	The fixed event will be set when there is a fix, and cleared when there is none
	"""
	return