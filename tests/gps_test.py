import os
import sys
from pytest import raises

# get main directory
__location__ = os.path.join(os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__))), "..")
# add it to sys path for imports to work
sys.path.insert(0, os.path.join(__location__))
# import project-level modules
from avc.GPS import GPS, GPS_Exception, Coordinate
from avc.ConfigReader import ConfigReader
from time import sleep


# TESTS:

def test_create_gps_object():
	gps_object = GPS(fakeconfig)
	assert isinstance(gps_object, GPS)

def test_gps_serial_connect_failure():
	gps_object = GPS(fakeconfig)
	gps_object.start()
	# let process attempt to start...
	sleep(0.5)
	# verify there was an exception raised by the process
	assert isinstance(gps_object.get_raised_exception(),Exception)

# overlapping tests
def test_gps_is_maximally_overlapping():
	gps = GPS(config)
	gps.current_coordinate = Coordinate(30.0000, -80.0000)
	test_coordinate = Coordinate(30.0000, -80.0000)
	assert gps.is_overlapping(test_coordinate)

def test_gps_is_minimally_overlapping():
	gps = GPS(config)
	# make overlap marginally smaller to account for float math error
	overlap = config["gps"]["minimum_overlap"]*0.9999
	gps.current_coordinate = Coordinate(30.0000, -80.0000)
	test_coordinates = []
	test_coordinates.append(Coordinate(30.0000+overlap, -80.0000))
	test_coordinates.append(Coordinate(30.0000-overlap, -80.0000))
	test_coordinates.append(Coordinate(30.0000, -80.0000-overlap))
	test_coordinates.append(Coordinate(30.0000, -80.0000+overlap))
	for coordinate in test_coordinates:
		print coordinate
		assert gps.is_overlapping(coordinate)

def test_gps_is_not_overlapping():
	gps = GPS(config)
	overlap = config["gps"]["minimum_overlap"]*2
	gps.current_coordinate = Coordinate(30.0000, -80.0000)
	test_coordinate = Coordinate(30.0000+overlap, -80.0000)
	assert not gps.is_overlapping(test_coordinate)

def test_gps_is_minimally_not_overlapping():
	gps = GPS(config)
	overlap = config["gps"]["minimum_overlap"]*1.0001
	gps.current_coordinate = Coordinate(30.0000, -80.0000)
	test_coordinates = []
	test_coordinates.append(Coordinate(30.0000+overlap, -80.0000))
	test_coordinates.append(Coordinate(30.0000-overlap, -80.0000))
	test_coordinates.append(Coordinate(30.0000, -80.0000-overlap))
	test_coordinates.append(Coordinate(30.0000, -80.0000+overlap))
	for coordinate in test_coordinates:
		print coordinate
		assert not gps.is_overlapping(coordinate)

# angle between nodes tests
def test_gps_angles_make_sense():
	gps = GPS(config)
	gps.current_coordinate = Coordinate(35.0000, 85.0000)
	test_fixtures = []
	test_fixtures.append( (Coordinate(36.0000, 85.0000), 90) ) # desired is East
	test_fixtures.append( (Coordinate(36.0000, 86.0000), 45) ) # desired is North-East
	test_fixtures.append( (Coordinate(35.0000, 86.0000), 0) ) # desired is North
	test_fixtures.append( (Coordinate(34.0000, 86.0000), -45) ) # desired is North-West
	test_fixtures.append( (Coordinate(34.0000, 85.0000), -90) ) # desired is West
	test_fixtures.append( (Coordinate(34.0000, 84.0000), -135) ) # desired is South-West
	test_fixtures.append( (Coordinate(35.0000, 84.0000), 180) ) # desired is South
	test_fixtures.append( (Coordinate(36.0000, 84.0000), 135) ) # desired is South-East
	test_fixtures.append( (Coordinate(35.0000, 85.0000), 0) ) # desired is Unchanged
	for coordinate,expected_angle in test_fixtures:
		calculated_angle = gps.calculate_angle_to_node(coordinate)
		print "calc: {}, expect: {}".format(calculated_angle,expected_angle)
		assert calculated_angle == expected_angle

# relative angle to goal test
def test_gps_relative_angle_to_goal():
	gps = GPS(config)
	gps.current_coordinate = Coordinate(35.0000, 85.0000)
	test_fixtures = []
	# Goal is to the East
	test_fixtures.append( (Coordinate(36.0000, 85.0000), 90, 0) ) # facing East
	test_fixtures.append( (Coordinate(36.0000, 85.0000), 45, 45) ) # facing North-East
	test_fixtures.append( (Coordinate(36.0000, 85.0000), 0, 90) ) # facing North
	test_fixtures.append( (Coordinate(36.0000, 85.0000), -45, 135) ) # facing North-West
	test_fixtures.append( (Coordinate(36.0000, 85.0000), -90, 180) ) # facing West
	test_fixtures.append( (Coordinate(36.0000, 85.0000), -135, -135) ) # facing South-West
	test_fixtures.append( (Coordinate(36.0000, 85.0000), 180, -90) ) # facing South
	test_fixtures.append( (Coordinate(36.0000, 85.0000), 135, -45) ) # facing South-East
	# Goal is to the North
	test_fixtures.append( (Coordinate(35.0000, 86.0000), 90, -90) ) # facing East
	test_fixtures.append( (Coordinate(35.0000, 86.0000), 45, -45) ) # facing North-East
	test_fixtures.append( (Coordinate(35.0000, 86.0000), 0, 0) ) # facing North
	test_fixtures.append( (Coordinate(35.0000, 86.0000), -45, 45) ) # facing North-West
	test_fixtures.append( (Coordinate(35.0000, 86.0000), -90, 90) ) # facing West
	test_fixtures.append( (Coordinate(35.0000, 86.0000), -135, 135) ) # facing South-West
	test_fixtures.append( (Coordinate(35.0000, 86.0000), 180, 180) ) # facing South
	test_fixtures.append( (Coordinate(35.0000, 86.0000), 135, -135) ) # facing South-East
	# Goal is to the West
	test_fixtures.append( (Coordinate(34.0000, 85.0000), 90, 180) ) # facing East
	test_fixtures.append( (Coordinate(34.0000, 85.0000), 45, -135) ) # facing North-East
	test_fixtures.append( (Coordinate(34.0000, 85.0000), 0, -90) ) # facing North
	test_fixtures.append( (Coordinate(34.0000, 85.0000), -45, -45) ) # facing North-West
	test_fixtures.append( (Coordinate(34.0000, 85.0000), -90, 0) ) # facing West
	test_fixtures.append( (Coordinate(34.0000, 85.0000), -135, 45) ) # facing South-West
	test_fixtures.append( (Coordinate(34.0000, 85.0000), 180, 90) ) # facing South
	test_fixtures.append( (Coordinate(34.0000, 85.0000), 135, 135) ) # facing South-East
	# Goal is to the South
	test_fixtures.append( (Coordinate(35.0000, 84.0000), 90, 90) ) # facing East
	test_fixtures.append( (Coordinate(35.0000, 84.0000), 45, 135) ) # facing North-East
	test_fixtures.append( (Coordinate(35.0000, 84.0000), 0, 180) ) # facing North
	test_fixtures.append( (Coordinate(35.0000, 84.0000), -45, -135) ) # facing North-West
	test_fixtures.append( (Coordinate(35.0000, 84.0000), -90, -90) ) # facing West
	test_fixtures.append( (Coordinate(35.0000, 84.0000), -135, -45) ) # facing South-West
	test_fixtures.append( (Coordinate(35.0000, 84.0000), 180, 0) ) # facing South
	test_fixtures.append( (Coordinate(35.0000, 84.0000), 135, 45) ) # facing South-East
	# test if expectations are met
	for coordinate,heading,expected_angle in test_fixtures:
		calculated_angle = gps.get_desired_heading(heading, coordinate)
		print "calc: {}, expect: {}".format(calculated_angle,expected_angle)
		assert calculated_angle == expected_angle 

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
