from avc.ConfigReader import ConfigReader
from avc.UserInput import UserInput
from avc.GPS import GPS, GPS_Exception
from time import sleep

# connect to GPS (connect + wait for fix)
# while not exited, print latest GPS coordinate
# if s is entered, current GPS coordinate is added to list
# if c is entered, a new nodes.json file is created -> displays chart showing coordinates


def node_terminal(config):
	# start gps
	gps = GPS(config)
	gps.start()
	# start user input thread
	userInput = UserInput()
	userInput.start()
	# wait for gps to be fixed
	print("waiting for gps fix...")
	gps.wait_for_fix()
	print("gps fix found!")
	gpslist = []
	while gps.is_properly_alive():
		user_inp = userInput.returnMessage()
		if user_inp is not None:
			user_inp = user_inp.lower()
			if user_inp == "exit":
				break
			elif user_inp == "a":
				gpslist.append(gps.get_location())
			elif user_inp == "s":
				pass
			elif user_inp == "c":
				pass

		sleep(0.2)

	gps.stop()
	userInput.stop()
	if gps.get_raised_exception() is not None:
		print(gps.get_raised_exception())
	for item in gpslist:
		print item


if __name__ == "__main__":
	config = ConfigReader.read_json("conf.json")
	print(config)
	node_terminal(config)
