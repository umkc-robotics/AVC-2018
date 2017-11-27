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
				sleep(0.05)
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
	max_vals = (max(data, key=lambda compass_data: compass_data.x).x, max(data, key=lambda compass_data: compass_data.y).y)
	min_vals = (min(data, key=lambda compass_data: compass_data.x).x, min(data, key=lambda compass_data: compass_data.y).y)
	print max_vals
	print min_vals
	# hard iron correction
	mag_bias = [0,0]
	mag_bias[0] = (max_vals[0] + min_vals[0])/2.0;
	mag_bias[1] = (max_vals[1] + min_vals[1])/2.0;
	#soft iron
	mag_scale = [0,0]
	mag_scale[0] = (max_vals[0] - min_vals[0])/2.0;
	mag_scale[1] = (max_vals[1] - min_vals[1])/2.0;

	avg_radius = (mag_scale[0] + mag_scale[1])/2.0

	mag_scales = [0,0]
	mag_scales[0] = float(avg_radius)/(mag_scale[0])
	mag_scales[1] = float(avg_radius)/(mag_scale[1])

	# saving into jsonify-able dictionaries
	biases = { "x": mag_bias[0], "y": mag_bias[1] }
	scales = { "x": mag_scales[0], "y": mag_scales[1] }
	calibration_data = { "bias": biases, "scalar": scales}
	return calibration_data


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
		if user_inp != None:
			user_inp = user_inp.lower()
			if user_inp == "exit":
				break
			elif user_inp == "c":
				calibration_data = perform_calibration(compass.get_and_reset_data())
				print calibration_data
				save_calibration_to_file(calibration_data)

		sleep(0.2)


	compass.stop()
	userInput.markToStop()
	print compass.get_raised_exception()


if __name__ == "__main__":
	config = ConfigReader.read_json("conf.json")
	print config
	calibration_terminal(config)
