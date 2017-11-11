from avc.AsyncDriver import ThreadDriver, ProcessDriver
from time import sleep


class ThreadTest(ThreadDriver):
	def __init__(self, target, args):
		self.count = 0
		ThreadDriver.__init__(self, target, args)
	
	def handle_input(self, input_obj):
		self.count = input_obj

class ThreadSelfTest(ThreadDriver):
	def __init__(self):
		self.count = 0
		ThreadDriver.__init__(self, print_stuff, ("ayylmao",))
	
	def handle_input(self, input_obj):
		self.count = input_obj

class ProcessSelfTest(ProcessDriver):
	def __init__(self):
		self.count = 0
		ProcessDriver.__init__(self, print_stuff, ("ayylmao",))
	
	def handle_input(self, input_obj):
		self.count = input_obj

	

class ProcessTest(ProcessDriver):
	def __init__(self, target, args):
		self.count = 0
		ProcessDriver.__init__(self, target, args)
	
	def handle_input(self, input_obj):
		self.count = input_obj




def see_if_thread_is_messed_up():
	total_objects = 5
	objects = []
	for i in range(0,total_objects):
		objects.append(ThreadTest(target=print_stuff,args=("ayylmao",)))
		#objects.append(ThreadSelfTest())
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
			#sleep(0.1)
	# if pipe is being closed, ignore it and close safely
	except Exception as e:
		try:
			comm_pipe.send(e)
		except IOError as e:
			pass