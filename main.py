from avc.ConfigReader import ConfigReader
from avc.GPS import GPS, GPS_Exception
from avc.AsyncDriver import ThreadDriver, ProcessDriver
from time import sleep


class ThreadTest(ThreadDriver):
	def __init__(self, target, args):
		self.count = 0
		ThreadDriver.__init__(self, target, args)
	
	def handle_input(self, input_obj):
		self.count = input_obj

class ProcessTest(ProcessDriver):
	def __init__(self, target, args):
		self.count = 0
		ProcessDriver.__init__(self, target, args)
	
	def handle_input(self, input_obj):
		self.count = input_obj




def test_see_if_thread_is_messed_up():
	total_objects = 3
	objects = []
	for i in range(0,total_objects):
		objects.append(ProcessTest(target=print_stuff, args=("ayylmao",)))
	for i in range(0,total_objects):
		objects[i].start()
	sleep(5)
	for i in range(0,total_objects):
		objects[i].stop()
	sleep(.1)
	for i in range(0,total_objects):
		print "Exception? {},{}".format(i,objects[i].raised_exception)
	for i in range(0,total_objects):
		print "Count: {},{}".format(i,objects[i].count)
	print "Total: {}".format(sum([x.count for x in objects]))
	print "done now"



def print_stuff(stuff, comm_pipe):
	keep_running = True
	count = 0
	try:
		while keep_running:
			if comm_pipe.poll():
				received = comm_pipe.recv()
				print received
				if received == "EXIT":
					print "Received SIGNAL TO EXIT"
					keep_running = False
			try:
				if count % 10 == 0:
					comm_pipe.send(count)
			except IOError as e:
				keep_running = False
				break
			count += 1
	# if pipe is being closed, ignore it and close safely
	except Exception as e:
		comm_pipe.send(e)

if __name__ == "__main__":
	test_see_if_thread_is_messed_up()

"""configReader = ConfigReader("conf.json")
config = configReader.get_config()

if __name__ == "__main__":
	gps = GPS(config)
	gps.start()

	while True:
		sleep(0.25)
		print "hello!"
		print gps.get_current_location()
		print gps.has_fix()"""
