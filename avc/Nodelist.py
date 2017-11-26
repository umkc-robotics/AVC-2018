import os
import json
from GPS import Coordinate
from ConfigReader import ConfigReader, ConfigReaderException

class Node(object):

	def __init__(self, json_object):
		self.json_object = json_object
		self.coordinate = self.create_coordinate(json_object)

	def get_coordinate(self):
		return self.coordinate

	def create_coordinate(self, json_object):
		coordinate = json_object["coordinate"]
		return Coordinate(coordinate["latitude"],coordinate["longitude"])

class Nodelist(object):

	def __init__(self, conf):
		self.conf = conf
		self.nodelist = Nodelist.read_node_file(self.conf["nodelist"]["file"])

	def get_list(self):
		return self.nodelist

	@staticmethod
	def read_node_file(location):
		raw_json = ConfigReader.read_json(location)
		nodelist = []
		for item in raw_json["nodes"]:
			nodelist.append(Node(item))
		return nodelist
