from avc.ConfigReader import ConfigReader
from avc.ArduinoComm import ArduinoComm, CommandException
from time import sleep

def arduino_console(config):
	arduino = ArduinoComm(config)
	arduino.start()
	# wait for arduino to be ready
	arduino.wait_for_readiness()
	
	try:
		user_input = ""
		while user_input != "EXIT":
			user_input = raw_input()
			input_list = user_input.strip().split()
			command = input_list[0]
			if command in ["f","b"]:
				try:
					value = int(str(int(input_list[1])))
					if command == "f":
						arduino.commandForward(value)
					elif command == "b":
						arduino.commandBackward(value)
				except IndexError as e:
					print "Bad Input: no second value found; {}".format(str(e))
				except ValueError as e:
					print "Bad input: value must be an integer; {}".format(str(e))
				except CommandException as e:
					print "Bad input: command formation failed; {}".format(str(e))
			elif command == "t":
				try:
					value = int(str(int(input_list[1])))
					arduino.commandTurn(value)
				except IndexError as e:
					print "Bad Input: no second value found; {}".format(str(e))
				except ValueError as e:
					print "Bad input: value must be an integer; {}".format(str(e))
				except CommandException as e:
					print "Bad input: command formation failed; {}".format(str(e))
			elif command == "stop":
				try:
					arduino.commandStop()
				except CommandException as e:
					print "Bad input: command formation failed; {}".format(str(e))
			elif command == "straight":
				try:
					arduino.commandStraight()
				except CommandException as e:
					print "Bad input: command formation failed; {}".format(str(e))
			elif command == "reset":
				try:
					arduino.commandReset()
				except CommandException as e:
					print "Bad input: command formation failed; {}".format(str(e))
	except Exception as e:
		print str(e)

	arduino.commandReset()
	sleep(1)
	arduino.stop()



if __name__ == "__main__":
	config = ConfigReader.read_json("conf.json")
	print config
	arduino_console(config)
