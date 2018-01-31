from avc.ConfigReader import ConfigReader
from avc.UserInput import UserInput
from avc.GPS import GPS, GPS_Exception

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

	while gps.is_properly_alive():
		user_inp = userInput.returnMessage()
		if user_inp is not None:
			user_inp = user_inp.lower()
			if user_inp == "exit":
				break

		sleep(0.2)

if __name__ == "__main__":
	config = ConfigReader.read_json("conf.json")
	print(config)
	node_terminal(config)
