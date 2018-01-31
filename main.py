from avc.ConfigReader import ConfigReader
from avc.GPS import GPS, GPS_Exception
from avc.Compass import Compass, CompassException
from avc.ArduinoComm import ArduinoComm
from avc.Nodelist import Nodelist
from time import sleep

def create_objects(config):
	# initialize nodelist
	nodelist = Nodelist(config)
	# start all processes
	gps = GPS(config)
	compass = Compass(config)
	arduino = ArduinoComm(config)
	gps.start()
	compass.start()
	arduino.start()
	# wait for arduino to be ready
	arduino.wait_for_readiness()
	# wait for gps to be fixed
	print("waiting for gps fix...")
	gps.wait_for_fix()
	print("gps fix found!")
	# wait for go button to be pressed
	print("waiting for go button press...")
	arduino.wait_for_button_press()
	print("go button pressed!")
	# get the first node
	node = nodelist.get_next_node()
	while not nodelist.all_nodes_visited() and gps.is_properly_alive() and compass.is_properly_alive() and arduino.is_properly_alive():
		# if at coordinate, get next node and start from top of loop
		if gps.is_overlapping(node):
			node = nodelist.get_next_node()
			continue
		desiredHeading = gps.get_desired_heading(compass.get_heading(), node)
		print(node.get_coordinate())
		print(gps.get_location())
		print(gps.calculate_angle_to_node(node.get_coordinate()))
		print(compass.get_heading())
		print("Desired: {}".format(desiredHeading))
		arduino.commandTurn(desiredHeading)
		sleep(0.1)
		arduino.commandForward(node.get_throttle())
		sleep(0.1)
	# stop car
	for i in range(0,10):
		arduino.commandReset()
		sleep(0.005)
	sleep(2)
	# print possible exceptions
	print("Exception ({}): {}".format("GPS",gps.get_raised_exception()))
	print("Exception ({}): {}".format("COMPASS",compass.get_raised_exception()))
	print("Exception ({}): {}".format("ARDUINO",arduino.get_raised_exception()))
	# stop all processes
	gps.stop()
	compass.stop()
	arduino.stop()
	print("done now!")


if __name__ == "__main__":
	config = ConfigReader.read_json("conf.json")
	print(config)
	create_objects(config)
