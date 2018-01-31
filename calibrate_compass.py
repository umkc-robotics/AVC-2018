from avc.Compass import Compass, CompassException, CompassData
from avc.ConfigReader import ConfigReader
from avc.UserInput import UserInput
from time import sleep
from matplotlib import pyplot
import matplotlib
import json



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
			print("RECEIVED WEIRD INPUT: {}".format(input_obj))



def perform_calibration(data):
	max_vals = (max(data, key=lambda compass_data: compass_data.x).x, max(data, key=lambda compass_data: compass_data.y).y)
	min_vals = (min(data, key=lambda compass_data: compass_data.x).x, min(data, key=lambda compass_data: compass_data.y).y)
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

def show_data(data):
	x_data = map(lambda item: item.x, data)
	y_data = map(lambda item: item.y, data)

	fig = matplotlib.pyplot.figure()
	ax = fig.add_subplot(111)

	ax.scatter(x_data,y_data)
	ax.axis([min(x_data),max(x_data),min(y_data),max(y_data)])
	matplotlib.pyplot.show()

def show_data_with_calibration(data, calibration_data):
	mag_bias = calibration_data["bias"]
	mag_scales = calibration_data["scalar"]
	corrected_data = map(lambda x: Compass.correct_data_point(x, mag_bias, mag_scales), data)
	show_data(corrected_data)

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
		if user_inp is not None:
			user_inp = user_inp.lower()
			if user_inp == "exit":
				break
			elif user_inp == "c":
				data_for_calibration = compass.get_and_reset_data()
				calibration_data = perform_calibration(data_for_calibration)
				print(calibration_data)
				save_calibration_to_file(config,calibration_data)
				show_data_with_calibration(data_for_calibration,calibration_data)
			elif user_inp == "s":
				show_data(compass.get_data())

		sleep(0.2)


	compass.stop()
	userInput.stop()
	if compass.get_raised_exception() is not None:
		print(compass.get_raised_exception())


if __name__ == "__main__":
	config = ConfigReader.read_json("conf.json")
	print(config)
	calibration_terminal(config)
