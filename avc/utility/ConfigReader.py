import json
import os

# directory from which this script is ran
__location__ = os.path.realpath(
	os.path.join(os.getcwd(), os.path.dirname(__file__)))
__location__ = os.path.join(__location__, "..")

# config reader exception class
class ConfigReaderException(Exception):
	pass

class ConfigReader(object):

	def __init__(self,location):
		self.readable_object = None
	
	def read_json(self,location):
		location = os.path.join(__location__,location)
		with open(location, "r") as json_file:
			self.readable_object = json.load(json_file)

	def get_conf(self):
		return self.readable_object
