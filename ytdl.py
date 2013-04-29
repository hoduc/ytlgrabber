from bs4 import BeautifulSoup
from httplib2 import *
import urllib.request
from urllib.request import urlopen
import urllib
import re
import unicodedata

#Keep links, video format for each, title
#id ?v=...[11 character]
class YouTube:
	def __init__(self):
		self.vl = []
		self.av_format = []
		self.title = ""
		self.desc = ""
		self.img = ""
		self.id = ""
	#tuple (format, direct link, size)
	def addVideoLink(self,vili):
		self.vl.append(vili)
	def addAvFormat(self,form):
		self.av_format.append(form)
	def getAvFormat(self):
		return self.av_format
	def setTitle(self, s):
		self.title = s
	def setDesc(self, d):
		self.desc = d
	def getTitle(self):
		return self.title
	def getDesc(self):
		return self.desc
	def setId(self, s):
		self.id = s
	def setImg(self,i):
		self.img = i
	def getId(self):
		return self.id
	def getImg(self):
		return self.img
	#only keep tracked of current link
	def clear(self):
		self.vl = []
		self.av_format = []
		self.title = ""
		self.img = ""
		
yt = YouTube()

#Tag : Dictionary of video format and its itag
itag = {
	"5"   : "240p   FLV",
	"6"   : "270p   FLV",
	"13"  : "N/A    3GP",
	"17"  : "144p   3GP",
	"18"  : "270p   MP4",
	"22"  : "720p   MP4",
	"34"  : "360p   FLV",
	"35"  : "480p   FLV",
	"36"  : "240p   3GP",
	"37"  : "1080p  MP4",
	"38"  : "3072p  MP4",
	"43"  : "360p   WebM",
	"44"  : "480p   WebM",
	"45"  : "720p   WebM",
	"46"  : "1080p  WebM",
	"82"  : "360p   MP4",
	"83"  : "240p   MP4",
	"84"  : "720p   MP4",
	"85"  : "520p   MP4",
	"100" : "360p   MP4",
	"101" : "360p   MP4",
	"102" : "720p   WebM",
	"120" : "720p   FLV"
}



#Helper function

#Check link against a rule set(reexp)
def matches(pattern, link):
	res = re.compile(pattern)
	res = re.search(pattern,link)
	if res != None:
		return True
	return False

def getLink(link):
	ytpattern = r"^(http://)?(www.)?(youtu)(.be|be.com)(/watch[?]v=)(.{11})$"
	if matches(ytpattern, link):
		#getting the directLink
		getDl(link)
		print("right")
		return True
	else:
		print("wrong")
		return False

#String and exception list[not to be replaced]
def percentDecode(s,excl):
	#1st pass
	s = urllib.parse.unquote(s)
	#2nd pass
#Open connection and get the html doc

def getDl(link):
	h = Http()
	response, content = h.request(link)
	if response.status == 200:
		print ("GetDL")
		soup = BeautifulSoup(content)
		title = soup.title.string
		yt.setTitle(str(title))
		counter = 0
		w7Con = soup.find('div',attrs={'id':'watch7-container'})
		rUrl = w7Con.find('link',attrs={'itemprop':'url'})
		rDesc = w7Con.find('meta',attrs={'itemprop':'description'})
		rImg = w7Con.find('link',attrs={'itemprop':'thumbnailUrl'})
		yt.setDesc(rDesc['content'])
		yt.setImg(rImg['href'])
		res = re.search(r"([?]v=)(.{11})$",rUrl['href'])
		if res != None:
			yt.setId(str(res.group(2)))		
		else:
			print ("hsaha")
		#highly inefficient
		longStr = w7Con.find('script').next_sibling.next_sibling
		res = re.search(r'\"fmt_list\": \"(.+?)\"',str(longStr.contents))
		if res != None:
			avform = res.group(1).split(",")
			print ("here")
			for e in avform:
				e = e[0:e.find("\\")]
				print (e)
			yt.addAvFormat(avform)
			print (yt.getAvFormat())
		else:
			print ("cannot find any!!!")
		res = re.search(r'\"url_encoded_fmt_stream_map\": \"(.+?)\"',str(longStr.contents))
		if res != None:
			dvidl = res.group(1).split(",")
			for e in dvidl:
				messylink = urllib.parse.unquote(urllib.parse.unquote(e))
				messylink = messylink.replace(",","%2C")
				link = ""
				res = re.search(r'url=(.+?)\\\\u0026',messylink)
				if res != None:
					url = res.group(1)
					print ("url=",url)
					res = re.search(r'sig=(.+?)\\\\u0026',messylink)
					if res != None:
						sig = "signature=" + res.group(1)
						print ("sig=",sig)
						link = url + "&" + sig
					else:
						print ("Cannot find sig")
				else:
					print ("Cannot find url!!!")
				
				
				#Connect to get the size
				#In progress
				print (link)
		else:
			print ("cannot find!!!")
			
	else:
		print ("Something wrong")



if __name__ == '__main__':
	if getLink("http://www.youtube.com/watch?v=gYvw68IneV4"):
		print (yt.getId())
		print (yt.getId())
		print (yt.getTitle())
		print (yt.getImg())
		print (yt.getDesc())
		print ("True")
	else: 
		print ("False")