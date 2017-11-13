from serial import Serial, SerialException
from collections import namedtuple
from time import sleep
from AsyncDriver import ThreadDriver, ProcessDriver


class Command(object):

	def __init__(self, command, values):
		self.command = command
		self.values = values

	def is_valid(self):
		pass

	def get_checksum(self, message):
		"""
		Returns a single character corresponding to calculated XOR checksum of message
		Returns: a single character
		"""
		checksum = 0
		for ch in message:
			checksum ^= ord(ch)
		return str(unichr(checksum))

	def get_formatted_string(self):
		pass

	@staticmethod
	def create_command(fullmessage):
		"""
		Returns a Command object initialized with a string, or None if string is not valid
		Returns: Command object OR None
		"""
		pass



class ArduinoCommException(Exception):
	pass



class ArduinoComm(ProcessDriver):

	def __init__(self, conf):
		self.conf = conf
		self.button_pressed = False
		ProcessDriver.__init__(self, arduino_process, (conf,))
		self.daemon = conf["daemon"]

	# Steering Commands
	def commandTurn(self, angle):
		pass

	def commandStraight(self, angle):
		pass

	# Throttle Commands
	def commandForward(self, speed):
		pass

	def commandBackward(self, speed):
		pass

	def commandStop(self):
		pass

	# Other Commands
	def commandResetButton(self):
		pass

	# Getters
	def is_pressed(self):
		return self.button_pressed

	# Input handler
	def handle_input(self, input_obj):
		pass

	# Send command through pipe
	def send_through_pipe(self, command):
		self.comm_pipe.send(command)



def arduino_process(conf, comm_pipe):
	arduino_serial = None
	print "ARDUINO PROCESS STARTED"
	try:
		keep_running = True
		# start serial process, raise a ArduinoComm exception if fails
		try:
			arduino_serial = Serial(conf["arduino"]["port"],conf["arduino"]["baud"])
		except SerialException as e:
			raise ArduinoCommException(e)
		print "CONNECTED TO ARDUINO"
		while keep_running:
			# check pipe for messages
			if comm_pipe.poll():
				received = comm_pipe.recv()
				if received == "EXIT":
					keep_running = False
					break
				elif isinstance(received, Command):
					pass
			# get serial input
			# validate checksum
			# turn into Command object
			# send proper serial response
			# send through pipe 

	except Exception as e:
		try:
			print "SENDING ERROR..."
			comm_pipe.send(e)
		except IOError as e:
			pass
	finally:
		if isinstance(arduino_serial,Serial):
			arduino_serial.close()
