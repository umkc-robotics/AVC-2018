import os
import sys
from pytest import raises

# get main directory
__location__ = os.path.join(os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))), "..")
# add it to sys path for imports to work
sys.path.insert(0, os.path.join(__location__))
# import project-level modules
from avc.GPS import GPS, GPS_Exception, ThreadDriver
from avc.ConfigReader import ConfigReader
from time import sleep





# TESTS:

def test_create_gps_object():
	gps_object = GPS(fakeconfig)
	assert isinstance(gps_object, GPS)

def test_gps_serial_connect_failure():
	gps_object = GPS(fakeconfig)
	with raises(GPS_Exception):
		gps_object.start()

def test_see_if_thread_is_fucked():
	thread_object = ThreadDriver()
	thread_object.start()
	sleep(1)
	print thread_object.raised_exception
	assert isinstance(thread_object.raised_exception, Exception)

# END TESTS






# setup objects for this module
def setup_module(module):
	configReader = ConfigReader("conf.json")
	fakeReader = ConfigReader("testconf.json")
	module.config = configReader.get_config()
	module.fakeconfig = fakeReader.get_config()

def teardown_module(module):
	pass
# done setting up objects for this module

# set up for each function
def setup_function(function):
	pass

def teardown_function(function):
	pass
# done setting up objects for each function
