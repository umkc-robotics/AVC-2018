from avc.ArduinoComm import ArduinoComm, ArduinoCommException
from avc.ArduinoComm import Command, CommandException
from time import sleep

if __name__=="__main__":
	#count = 0
	#for n in range(0,1000000):
	#	newcommand = Command("s")
	#	#count += 1;
	newcommand = Command("reset","ayylmaoC")
	print newcommand
	print len(str(newcommand))
	print str(newcommand)[-1]
	print ord(str(newcommand)[-1])
