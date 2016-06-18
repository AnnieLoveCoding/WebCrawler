from html.parser import HTMLParser
from urllib import parse

#inherite HTMLParser
#this class can search the link in html file and add the link to set

class linkSearcher(HTMLParser):
	
	#implement all method from the base class
	def __init__(self, home_page, page_url):
		super().__init__()
		self.home_page = home_page
		self.page_url = page_url
		#gather links in linkSet
		self.linkSet = set()
		
		
	def error(self, message):
		pass
		
	def handle_starttag(self, tag, attrs):
		#if a link is found
		if tag == 'a':
			#find href In the href attribute of the link, a relative url s used
			for (att, val) in attrs:
				if att == 'href':
					#if value if already full url, it will not add the base url again
					url = parse.urljoin(self.home_page, val)
					self.linkSet.add(url)
	
	
	def getLinkSet(self):
		return self.linkSet
					
		
