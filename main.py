from avc.ConfigReader import ConfigReader
from avc.GPS import GPS, GPS_Exception
from avc.Compass import Compass, CompassException
from time import sleep

def create_objects(config):
	gps = GPS(config)
	compass = Compass(config)
	gps.start()
	compass.start()
	while gps.is_properly_alive() and compass.is_properly_alive():
		if gps.is_fixed():
			print "Location: {}".format(gps.get_location())
		else:
			print "No fix yet"
		if compass.is_connected():
			print "Heading: {}".format(compass.get_heading())
		else:
			print "Compass NOT connected"
		sleep(0.5)
	print "Exception: {}".format(gps.get_raised_exception())
	print "Exception: {}".format(compass.get_raised_exception())
	gps.stop()
	compass.stop()
	print "done now!"


if __name__ == "__main__":
	config = ConfigReader.read_json("conf.json")
	print config
	create_objects(config)
