from dataFunction import * 
from linkSearcher import linkSearcher
from urllib.request import urlopen
#urlopen return byte, need to decode


import threading
from queue import Queue

from getDomain import *



class Spider:
	#shared resource
	
	folder_name = ''
	home_page = ''
	#only crawl the link in this domain
	domain_name = ''
	#need set for threading to read data instead of reading reom file every time
	readySet = set()
	waitingSet = set()
	ready_file = ''
	waiting_file = ''
	
	def __init__(self, folder_name, base_url, domain_name):
		Spider.folder_name = folder_name
		Spider.home_page = base_url
		Spider.domain_name = domain_name
		
		#self file path
		Spider.ready_file = Spider.folder_name + '/crawledLinks.txt'
		Spider.waiting_file = Spider.folder_name + '/waitingLinks.txt'
		
		#first spider do the preparation work(boot) and crawled the homapage
		self.boot()
		self.crawl_page('First spider', Spider.home_page)
		
	#create the project directory and two files
	@staticmethod
	def boot():
		create_webFolder_dir(Spider.folder_name)
		create_file(Spider.folder_name, Spider.home_page)
		Spider.readySet = file_to_set(Spider.ready_file)
		Spider.waitingSet = file_to_set(Spider.waiting_file)
		
	@staticmethod
	def crawl_page(thread_name, link):
		if link not in Spider.readySet:
			print(thread_name + " is crawling " + link)
			print(str(len(Spider.readySet)) + " links have been crawled!")
			print(str(len(Spider.waitingSet)) + " links are waiting to be crawled!")
			
			secondaryLinkSet = Spider.gatherLinks(link)
			Spider.LinksToWaitingSet(secondaryLinkSet)
			
			Spider.waitingSet.remove(link)
			Spider.readySet.add(link)
			
			#update the files once one page if one link finish being crawled
			Spider.update_files()
			
			
	@staticmethod
	def gatherLinks(link):
		html_string = ''
		try:
			response = urlopen(link)
			
			if 'text/html' in response.getheader('Content-Type'):
				html_byte = response.read()
				#convert byte to utf-8 double quote
				html_string = html_byte.decode("utf-8")
							
			searcher = linkSearcher(Spider.home_page, link)
			searcher.feed(html_string)
						
		except Exception as e:
			print(str(e))
			return set()
		return searcher.getLinkSet()
			
					
	@staticmethod
	def LinksToWaitingSet(linksSet):
		for url in linksSet:
			if url in Spider.waitingSet:
				continue
			if url in Spider.readySet:
				continue
			if Spider.domain_name != get_domain_name(url):
				continue
			Spider.waitingSet.add(url)
		
				
	
	@staticmethod
	def update_files():
		set_to_file(Spider.readySet, Spider.ready_file)
		set_to_file(Spider.waitingSet, Spider.waiting_file)
		

	
	
	
	