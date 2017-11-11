from avc.ConfigReader import ConfigReader
from avc.GPS import GPS, GPS_Exception
from time import sleep

def create_gps_object(config):
	gps = GPS(config)
	gps.start()
	while gps.is_properly_alive():
		if gps.is_fixed():
			print "Location: {}".format(gps.get_location())
		else:
			print "No fix yet"
		sleep(2)
	print "Exception: {}".format(gps.get_raised_exception())
	print "done now!"


if __name__ == "__main__":
	config = ConfigReader.read_json("conf.json")
	print config
	create_gps_object(config)

	#config = configReader.get_config()

"""configReader = ConfigReader("conf.json")
config = configReader.get_config()

if __name__ == "__main__":
	gps = GPS(config)
	gps.start()

	while True:
		sleep(0.25)
		print "hello!"
		print gps.get_current_location()
		print gps.has_fix()"""
