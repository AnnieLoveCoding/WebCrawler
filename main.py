import threading
from queue import Queue

from getDomain import *
from dataFunction import *
from Spider import Spider

PROJECT_NAME = 'AnnieLoveCoding'
HOMEPAGE = 'http://www.liaoxuefeng.com/'
DOMAIN_NAME = get_domain_name(HOMEPAGE)
QUEUE_FILE = PROJECT_NAME + '/waitingLinks.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawledLinks.txt'
NUMBER_OF_THREADS = 8
queue = Queue()


Spider(PROJECT_NAME, HOMEPAGE, DOMAIN_NAME)

#daemon : when your program quits, any daemon threads are killed automatically.
def create_workers():
	for _ in range(NUMBER_OF_THREADS):
		t = threading.Thread(target = work)
		t.daemon = True
		t.start()
		
#do next job in queue
def work():
	while True:
		url = queue.get()
		Spider.crawl_page(threading.current_thread().name, url)
		queue.task_done()
		
		

#crawl the links in queue is queue is not empty

def crawl():
	queue_links = file_to_set(QUEUE_FILE)
	if(len(queue_links)) > 0:
		print(str(len(queue_links)) + "links in queue")
		for link in file_to_set(QUEUE_FILE):
			queue.put(link)
		queue.join()
		crawl()
		
create_workers()
crawl()
