from avc.Compass import Compass, CompassException, CompassData
from avc.ConfigReader import ConfigReader
from time import sleep
from multiprocessing import Pipe
from matplotlib import pyplot
import threading
import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pygame
import pylab
import json

pygame.init()

# get user input in a separate thread
class UserInput(threading.Thread):
	
	def __init__(self):
		threading.Thread.__init__(self)
		parent_conn,child_conn = Pipe()
		self.pipeOutside = parent_conn
		self.pipeInside = child_conn
		self.keepGoing = threading.Event()
		self.newMessage = threading.Event()
		self.daemon = True # turn off if main thread turns off
	
	def getPipe(self):
		return self.pipeOutside
	
	def run(self):
		while not self.keepGoing.is_set():
			# wait until message is read
			if self.newMessage.is_set():
				time.sleep(0.05)
				continue
			userinp = raw_input('> ')
			if userinp.lower() == 'exit':
				self.markToStop()
			self.pipeInside.send(userinp)
			self.newMessage.set()
	
	def markMessageRead(self):
		self.newMessage.clear()
	
	def markToStop(self):
		self.keepGoing.set()
	
	def isNewMessage(self):
		return self.newMessage.is_set()
	
	def returnMessage(self):
		if self.isNewMessage():
			user_inp = self.pipeOutside.recv()
			self.markMessageRead()
			return user_inp
		else:
			return None



class CompassCalibrator(Compass):

	def __init__(self, conf):
		Compass.__init__(self, conf)
		self.current_data = []

	def append_data(self, data):
		self.current_data.append(data)

	def get_data(self):
		return list(self.current_data)

	def get_and_reset_data(self):
		list_to_return = list(self.current_data)
		self.current_data = []
		return list_to_return

	def handle_input(self, input_obj):
		if isinstance(input_obj, CompassData):
			self.append_data(input_obj)
		elif isinstance(input_obj, bool):
			self.compass_connected = input_obj
		else:
			print "RECEIVED WEIRD INPUT: {}".format(input_obj)



def perform_calibration(data):
	pass

def save_calibration_to_file(config,calibration_data):
	with open(config["compass"]["file"], "w") as calibration_file:
		calibration_file.write(json.dumps(calibration_data))

def calibration_terminal(config):
	# start compass
	compass = CompassCalibrator(config)
	compass.start()
	# start user input thread
	userInput = UserInput()
	userInput.start()

	while compass.is_properly_alive():
		user_inp = userInput.returnMessage()
		print compass.get_data()
		if user_inp != None:
			if user_inp.lower() == "exit":
				break
		sleep(1)


	compass.stop()
	userInput.markToStop()
	print compass.get_raised_exception()


if __name__ == "__main__":
	config = ConfigReader.read_json("conf.json")
	print config
	calibration_terminal(config)
