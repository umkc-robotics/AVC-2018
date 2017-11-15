from serial import Serial, SerialException
from collections import namedtuple
from time import sleep
from AsyncDriver import ThreadDriver, ProcessDriver

class CommandException(Exception):
	pass

class ArduinoCommException(Exception):
	pass



class Command(object):

	special_chars = ["|","*"]

	def __init__(self, command, values=None):
		self.values = None
		self.set_command(command)
		if values is not None:
			self.set_values(values)

	def set_command(self, command):
		"""
		Sets command, raises CommandException if proposed command is not valid
		Raises: CommandException on commands that contain special characters
		"""
		if not isinstance(command, str):
			raise CommandException("command must be a string, not {}".format(type(command)))
		elif any(ch in command for ch in self.special_chars):
			raise CommandException("command cannot include '|' or '*' characters")
		else:
			self.command = command

	def set_values(self, values):
		"""
		Sets values, raises CommandException if proposed values are not valid
		:param values: lsit or string (string valid for a single value)
		Raises: CommandException on values that contain special characters
		"""
		proper_type = False
		if isinstance(values, str):
			proper_type = True
			if not self.is_valid_string(values):
				raise CommandException("values cannot include '|' or '*' characters")
		elif isinstance(values, list):
			proper_type = True
			for value in values:
				if not self.is_valid_string(value):
					raise CommandException("values cannot include '|' or '*' characters")
		# if proper type, assign value
		if proper_type:
			self.values = values
		# otherwise, raise exception
		else:
			raise CommandException("values must be a string or a list, not {}".format(type(values)))

	def is_valid_string(self, string):
		"""
		Returns True/False depending on if string contains special characters
		Returns: boolean for validity
		"""
		return not any(ch in string for ch in self.special_chars)

	def get_formatted_string(self):
		"""
		Returns full string command to be sent to a device
		Preconditions: assumes command and values have been set properly
		Returns: string
		"""
		fullstring = ""
		argument_list = []
		argument_list.append(self.command)
		# if none, ignore
		if self.values is None:
			pass
		# if list, extend argument list
		elif isinstance(self.values,list):
			argument_list.extend(self.values)
		# if (hopefully) string, add it as an item
		else:
			argument_list.append(self.values)
		# add to fullstring
		fullstring = "|".join(argument_list)
		# add checksum to the end
		fullstring += "*{}".format(Command.get_checksum(fullstring))
		return fullstring

	def __str__(self):
		"""
		Wrapper for get_formatted_string()
		"""
		return self.get_formatted_string()

	@staticmethod
	def create_command(fullmessage):
		"""
		Returns a Command object initialized with a string, or None if string is not valid
		Returns: Command object OR None
		"""
		pass

	@staticmethod
	def get_checksum(message):
		"""
		Returns a single character corresponding to calculated XOR checksum of message
		Returns: a single character
		"""
		checksum = 0
		for ch in message:
			checksum ^= ord(ch)
		# change range of checksum
		checksum = (checksum % 94) + 33
		return str(unichr(checksum))



class ArduinoComm(ProcessDriver):

	def __init__(self, conf):
		self.conf = conf
		self.button_pressed = False
		ProcessDriver.__init__(self, arduino_process, (conf,))
		self.daemon = conf["daemon"]

	# Steering Commands
	def commandTurn(self, angle):
		cmd = Command("t",angle)
		self.send_through_pipe(cmd)

	def commandStraight(self):
		cmd = Command("s")
		self.send_through_pipe(cmd)

	# Throttle Commands
	def commandForward(self, speed):
		cmd = Command("f",speed)
		self.send_through_pipe(cmd)

	def commandBackward(self, speed):
		cmd = Command("b",speed)
		self.send_through_pipe(cmd)

	def commandStop(self):
		cmd = Command("stop")
		self.send_through_pipe(cmd)

	# Other Commands
	def commandResetButton(self):
		cmd = Command("rst")
		self.send_through_pipe(cmd)

	# Getters
	def is_pressed(self):
		return self.button_pressed

	# Input handler
	def handle_input(self, input_obj):
		if isinstance(input_obj,Command):
			# check if Go Button pressed command
			if input_obj.command = "gb":
				self.button_pressed = True
			# check if Low Battery command
			elif input_obj.command = "lb":
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
