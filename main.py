from avc.ConfigReader import ConfigReader
from avc.GPS import GPS, GPS_Exception
from time import sleep


configReader = ConfigReader("conf.json")
config = configReader.get_config()

if __name__ == "__main__":
	gps = GPS(config)
	gps.start()

	while True:
		sleep(0.25)
		print "hello!"
		print gps.get_current_location()
		print gps.has_fix()
