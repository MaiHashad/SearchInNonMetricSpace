import threading
import queue
import random
import os
import time
import csv
import hashlib
import shutil

log_name = "log_out/log.txt"
pending_comp = queue.SimpleQueue() # Of the format [main_uid, test_uid_A, test_uid_B]
finished_comp = queue.SimpleQueue() #Of the format [main_uid, closer_uid]
page_load_ack = queue.SimpleQueue() #Of the format [main_uid]
next_uid = 0
final_uid = len(list(filter(lambda x: x[0]!=".", os.listdir("pics")))) #used for checking limits
print("final_uid: {}".format(final_uid))
next_code_idx = 3000

# Stores all relevant data about a picture
class Picture():
	def __init__(self, filename):
		global next_uid
		self.name = filename
		self.uid = next_uid
		next_uid += 1
		self.nearest_neighbors = list(filter(lambda x: x != self.uid,list(range(final_uid))))
		random.shuffle(self.nearest_neighbors)

class PendingEntry():
	# Each of these attributes is a picture object
	def __init__(self, main_pic, comp_a, comp_b):
		global next_code_idx
		self.main_pic = main_pic
		self.comp_a = comp_a
		self.comp_b = comp_b
		self.code = "NULL"
		with open("code_master.txt", "r") as f:
			for i, line in enumerate(f):
				if i == next_code_idx:
					self.code = line.strip()
					next_code_idx+=1
					break

class AckEntry():
	def __init__(self, main_pic_uid):
		self.main_pic_uid = main_pic_uid

class FinishedEntry():
	# Each of these attributes is an integer
	def __init__(self, main_pic_name, closer_pic_name, further_pic_name):
		self.main_pic_name = main_pic_name
		self.closer_pic_name = closer_pic_name
		self.further_pic_name = further_pic_name
		#TODO: Maybe handling for further pic

# Return True if the test value is closer than the pivot
def compare_closeness(main_pic, test, pivot,log):
	print(threading.get_ident(), " ! main: ", main_pic.name)
	print(threading.get_ident(), " ! a: ", test.name)
	print(threading.get_ident(), " ! b: ", pivot.name)

	# Check the current data for this pic
	data = list(csv.reader(open("out/{}.csv".format(main_pic.uid), "r")))
	if str(test.uid) in data[pivot.uid]:
		# We've already decided pivot is closer than test
		return False
	elif str(pivot.uid) in data[test.uid]:
		# We've already decided test is closer than pivot
		return True

	found_response = False
	while not(found_response):
		# Place request on queue
		print("Putting request in queue for {}".format(main_pic.name))
		pending_comp.put(PendingEntry(main_pic = main_pic, comp_a = test, comp_b = pivot))

		# Keep reading ack queue looking for this pic
		foundAck = False
		while(True):
			ack_entry = page_load_ack.get()
			if ack_entry.main_pic_uid != main_pic.uid:
				# If it's not the one we're looking for, put it back
				page_load_ack.put(ack_entry)
				sleep_time = random.randint(1,10)
				time.sleep(sleep_time)
			else:
				start_time = time.time()
				break

		print("Page loaded for {}. Awaiting response for 60 seconds".format(main_pic.name))
		# Keep checking for a response for 60 seconds
		while(time.time() < start_time + 60):
			try:
				result = finished_comp.get(timeout=5)
			except:
				# Exception raised if queue was empty. Catch it and go back to top of loop
				continue
			
			if result.main_pic_name != main_pic.name:
				# If it's not the one we're looking for, put it back
				finished_comp.put(result)
				sleep_time = random.randint(1,10)
				time.sleep(sleep_time)
			else:
				print("Found response for {}".format(main_pic.name))
				if result.closer_pic_name == test.name and result.further_pic_name == pivot.name:
					found_response = True
					# Test value is closer than pivot
					log.write("{}: {} < {}\n".format(main_pic.uid, test.uid, pivot.uid))
					test_closer = True
					break
				elif result.closer_pic_name == pivot.name and result.further_pic_name == test.name:
					found_response = True
					# Test value is not closer than pivot
					log.write("{}: {} < {}\n".format(main_pic.uid, pivot.uid, test.uid))
					test_closer = False
					break
				else:
					# On invalid response, keep looking
					pass

	# update the data for this pic
	if test_closer:
		data[test.uid].append(pivot.uid)
	else:
		data[pivot.uid].append(test.uid)

	with open("out/{}.csv".format(main_pic.uid), "w") as write_file:
		wr = csv.writer(write_file)
		wr.writerows(data)

	return test_closer


# Standard partition, modified to act on picture object
def partition(picture,low,high, log, pic_array):
    i = (low - 1)
    x = picture.nearest_neighbors[high]
    for j in range(low,high):     #for j = p to r-1
        if compare_closeness(picture, pic_array[picture.nearest_neighbors[j]], pic_array[x], log):       #if the compared value is bigger than the pivot value
            i+= 1
            picture.nearest_neighbors[i],picture.nearest_neighbors[j] = picture.nearest_neighbors[j],picture.nearest_neighbors[i]

    picture.nearest_neighbors[i+1],picture.nearest_neighbors[high] = picture.nearest_neighbors[high],picture.nearest_neighbors[i+1]
    return (i + 1)

# Standard quick_sort, modified to act on picture object
def quick_sort(picture,low,high, log, pic_array):
    log.write("Sorting {}: {}\n".format(picture.uid, picture.nearest_neighbors[low:high]))
    if low>=high:
        return picture.nearest_neighbors   #already sorted
    pivot = partition(picture,low,high, log, pic_array)
    low = quick_sort(picture,low,pivot - 1, log, pic_array)      #sort everything before pivot
    high = quick_sort(picture,pivot + 1, high, log, pic_array)#sort everything after pivot
    return low + [pivot] + high


def sorter(picture, log, pic_array):
	sorted_array = quick_sort(picture, 0, len(picture.nearest_neighbors)-1, log, pic_array)
	f = open("log_out/{}_sorted.txt".format(picture.uid), "w")
	f.write("UID: {}\n".format(picture.uid))
	f.write("Name: {}\n".format(picture.name))
	f.write("{}".format(picture.nearest_neighbors))
	log.write("Finished sorting {}\n".format(picture.uid))


# Images will be stored in directory called "pics"
# Read the directory, initialize them, and return array
def init_pics():
	global next_uid
	pic_array = []
	pic_names = os.listdir("pics")

	for i in range(len(pic_names)):
		if pic_names[i][0] != ".":
			pic_array.append(Picture(pic_names[i]))

	f = open("pic_filenames.txt", "w")
	for picture in pic_array:
		f.write("{}: {}\n".format(picture.uid, picture.name))
	f.close()

	if next_uid != final_uid:
		print("Something went wrong generating this...")
		return None


	return pic_array

# ONLY RUN FIRST TIME
def init_data_files():
	print("THIS WILL ERASE EVERYTHING PRIOR TO THIS")
	sure_count = 0
	while sure_count < 3:
		answer = input("ARE YOU SURE? (Y/N)")
		if answer == "y" or answer == "Y":
			sure_count += 1
		else:
			return
	
	log = open(log_name, "w")

	# Init pic array, create pic_filenames file
	pic_array = init_pics()
	if pic_array == None:
		print("Error: Failed to init")

	# Make a new csv file with a bunch of newlines
	array = [[]]*final_uid
	for picture in pic_array:
		with open("out/{}.csv".format(picture.uid), "w") as write_file:
			writer = csv.writer(write_file)
			writer.writerows(array)


# Read pic_ids from file already created, and create pic_array
def read_pic_ids():
	f = open("pic_filenames.txt")
	lines = f.readlines()
	pic_array = []

	for line in lines:
		words = line.split(": ")
		uid = int(words[0])
		filename = words[1].strip()

		new_pic = Picture(filename)
		new_pic.uid = uid # Manually reset uid to match file
		pic_array.append(new_pic)

	return pic_array

def use_data_files():
	# Startup, get log file handles
	log = open(log_name, "a")

	# Create an array of Picture objects from files in /pics
	pic_array = read_pic_ids()

	sort_threads = []
	for i in range(len(pic_array)):
		t = threading.Thread(target=sorter, args=(pic_array[i], log, pic_array))
		sort_threads.append(t)
		t.start()


def generate_codes():
	f_m = open("code_master.txt", "w")
	for hash_seed in range(60000):
		code = hashlib.md5(str(hash_seed).encode()).hexdigest()
		f_m.write("{}\n".format(code))
	f_m.close()
