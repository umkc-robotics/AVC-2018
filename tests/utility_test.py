import os
import sys

# get main directory
__location__ = os.path.join(os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))), "..")
# add it to sys path for imports to work
sys.path.insert(0, os.path.join(__location__))
# import project-level modules
from avc.ConfigReader import ConfigReader



# TESTS BEGIN

def test_config_is_dictionary():
	assert isinstance(ConfigReader.read_json("conf.json"), dict)

# TESTS END



# setup objects for this module
def setup_module(module):
	pass

def teardown_module(module):
	pass
# done setting up objects for this module

# set up for each function
def setup_function(function):
	pass

def teardown_function(function):
	pass
# done setting up objects for each function
