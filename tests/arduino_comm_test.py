import os
import sys
from pytest import raises
# get main directory
__location__ = os.path.join(os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))), "..")
# add it to sys path for imports to work
sys.path.insert(0, os.path.join(__location__))
# import project-level modules

from avc.ArduinoComm import ArduinoComm, ArduinoCommException
from avc.ArduinoComm import Command, CommandException
from time import sleep


# setup objects for this module
def setup_module(module):
	module.config = ConfigReader.read_json("conf.json")
	module.fakeconfig = ConfigReader.read_json("testconf.json")

def teardown_module(module):
	pass
# done setting up objects for this module

# set up for each function
def setup_function(function):
	pass

def teardown_function(function):
	pass
# done setting up objects for each function