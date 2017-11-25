from avc.ConfigReader import ConfigReader
from avc.GPS import GPS, GPS_Exception
from avc.Compass import Compass, CompassException
from avc.ArduinoComm import ArduinoComm
from time import sleep

def create_objects(config):
	# start all processes
	gps = GPS(config)
	compass = Compass(config)
	arduino = ArduinoComm(config)
	gps.start()
	compass.start()
	arduino.start()
	# wait for arduino to be ready
	arduino.wait_for_readiness()
	# wait for go button to be pressed
	arduino.wait_for_button_press()
	
	while gps.is_properly_alive() and compass.is_properly_alive() and arduino.is_properly_alive():
		if gps.is_fixed():
			print "Location: {}".format(gps.get_location())
		else:
			print "No fix yet"
		if compass.is_connected():
			print "Heading: {}".format(compass.get_heading())
		else:
			print "Compass NOT connected"
		sleep(0.1)
	# print possible exceptions
	print "Exception ({}): {}".format("GPS",gps.get_raised_exception())
	print "Exception ({}): {}".format("COMPASS",compass.get_raised_exception())
	print "Exception ({}): {}".format("ARDUINO",arduino.get_raised_exception())
	# stop all processes
	gps.stop()
	compass.stop()
	arduino.stop()
	print "done now!"


if __name__ == "__main__":
	config = ConfigReader.read_json("conf.json")
	print config
	create_objects(config)
