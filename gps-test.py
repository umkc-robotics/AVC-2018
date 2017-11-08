from gps.GPS import GPS
from utility.ConfigReader import ConfigReader
import unittest

config = ConfigReader("conf.json")

class GPSTest(unittest.TestCase):

	def creation_test(self):
		"""
		Passes if GPS class can be instantiated with no exceptions
		"""
		return

if __name__ == "__main__":
	GPSTest.main()
	# run the tests...