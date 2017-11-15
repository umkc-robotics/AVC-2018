from avc.ArduinoComm import ArduinoComm, ArduinoCommException
from avc.ArduinoComm import Command, CommandException
from time import sleep
from random import randint, sample
from collections import OrderedDict


def generate_random_strings_with_checksum(repeats):
	for n in range(0,repeats):
		commandString = ""
		for n in range(randint(1,11)):
			commandString += str(unichr(randint(33,126)))
		try:
			newcommand = Command(commandString)
		except CommandException as e:
			print "{} --> {}".format(str(e),commandString)
		else:
			print "------"
			print newcommand
			print ord(str(newcommand)[-1])
			print "------"

def get_common_checksums_wrapper(max_length, min_char=33, max_char=126):
	common_dict = {}
	message = ""
	character_list = range(min_char,max_char+1)
	get_common_checksums(common_dict, message, max_length, character_list)
	return common_dict

def get_common_checksums(common_dict, message, max_length, character_list):
	if len(message) > max_length:
		return False
	for n in range(33,127):
		new_message = message + str(unichr(n))
		try:
			formatted_message = str(Command(new_message))
		except CommandException as e:
			continue
		checksum_char = formatted_message[-1]
		#common_dict.setdefault(checksum_char,[]).append(formatted_message)
		if len(message) == max_length:
			common_dict.setdefault(checksum_char,0)
			common_dict[checksum_char] += 1
		if not get_common_checksums(common_dict, new_message, max_length):
			break
	return True

def get_common_checksums_sparse_wrapper(max_length, sparse_value=94, min_char=33, max_char=126):
	common_dict = {}
	message = ""
	character_list = range(min_char,max_char+1)
	sparse_value = min(sparse_value, 94)
	get_common_checksums_sparse(common_dict, message, max_length, sparse_value, character_list)
	return common_dict

def get_common_checksums_sparse(common_dict, message, max_length, sparse_value, character_list):
	if len(message) > max_length:
		return False
	#sparse_characters_to_use = sorted(sample(character_list,sparse_value))
	sparse_characters_to_use = sample(character_list,sparse_value)
	#print sparse_characters_to_use
	for n in sparse_characters_to_use:
		new_message = message + str(unichr(n))
		try:
			formatted_message = str(Command(new_message))
		except CommandException as e:
			continue
		checksum_char = formatted_message[-1]
		#common_dict.setdefault(checksum_char,[]).append(formatted_message)
		if len(message) == max_length:
			common_dict.setdefault(checksum_char,0)
			common_dict[checksum_char] += 1
		if not get_common_checksums_sparse(common_dict, new_message, max_length, sparse_value, character_list):
			break
	return True

def combine_dicts(dict1,dict2):
	for key in dict2.keys():
		dict1.setdefault(key,0)
		dict1[key] += dict2[key]

def print_dict(dict1):
	for key,value in sorted(dict1.iteritems()):
		print "{}: {}".format(key,value)

if __name__=="__main__":
	old_dict = {}
	min_char = 97#33
	max_char = 122#126
	sparse_value = 3
	repetitions = 1
	for n in range(repetitions):
		new_dict = get_common_checksums_sparse_wrapper(11,sparse_value,min_char,max_char)
		combine_dicts(old_dict,new_dict)
	print_dict(old_dict)

	print "-----"

	#other_dict = get_common_checksums_wrapper(3)
	#print_dict(other_dict)
