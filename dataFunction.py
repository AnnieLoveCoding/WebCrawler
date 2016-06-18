import os


def create_webFolder_dir(project_name):
	if not os.path.exists(project_name):
		print("Creating the forlder for the crawler: " + project_name)
		os.makedirs(project_name)


def create_file(project_name, base_url):
	waitingQueue = os.path.join(project_name , 'waitingLinks.txt')
	readyQueue = os.path.join(project_name,"crawledLinks.txt")
	
	if not os.path.isfile(waitingQueue):
		write_file(waitingQueue, base_url)
		
	if not os.path.isfile(readyQueue):
		write_file(readyQueue, '')


def write_file(directory, data):
	with open(directory, 'w') as f:
		f.write(data)



def file_to_set(file_name):
	res = set()
	with open(file_name, 'rt') as f:
		for link in f:
			res.add(link.replace('\n', ''))
	return res



def set_to_file(linkSet, file_name):
	with open(file_name,"w") as f:
		for link in sorted(linkSet):
			f.write(link +"\n")
