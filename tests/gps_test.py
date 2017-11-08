import os
import sys

# get main directory
__location__ = os.path.join(os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))), "..")
# add it to sys path for imports to work
sys.path.insert(0, os.path.join(__location__))
# import project-level modules
from avc.gps.GPS import GPS
from avc.utility.ConfigReader import ConfigReader





# TESTS:

def test_create_gps_object():
	gps_object = GPS(config)
	assert isinstance(gps_object, GPS)

# END TESTS






# setup objects for this module
def setup_module(module):
	configReader = ConfigReader("conf.json")
	module.config = configReader.get_conf()

def teardown_module(module):
	pass
# done setting up objects for this module

# set up for each function
def setup_function(function):
	pass

def teardown_function(function):
	pass
# done setting up objects for each function