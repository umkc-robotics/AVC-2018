import os
import sys
from pytest import raises
# get main directory
__location__ = os.path.join(os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))), "..")
# add it to sys path for imports to work
sys.path.insert(0, os.path.join(__location__))
# import project-level modules

from time import sleep
from avc.ConfigReader import ConfigReader, ConfigReaderException
from avc.Nodelist import Nodelist

# TESTS

def test_creating_nodelist_object():
	nodelist = Nodelist(config)
	assert isinstance(nodelist, Nodelist)

def test_list_exists():
	nodelist = Nodelist(config)
	assert isinstance(nodelist.get_list(),list)

def test_list_contains_coordinates():
	nodelist = Nodelist(config)
	actual_list = nodelist.get_list()
	for item in actual_list:
		coordinate = item.coordinate
		assert isinstance(coordinate.latitude,float)
		assert isinstance(coordinate.longitude,float)

# END TESTS


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
