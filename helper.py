from YouTube import *
from bs4 import BeautifulSoup
from httplib2 import *
import urllib.request
from urllib.request import urlopen
import urllib
import re
import unicodedata
import json
import urllib.parse


h = Http()


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
		if getDl(link):
			return True
		return False
	else:
		print("Wrong Youtbe format")
		return False

def findByPat(patl, s):
	for e in patl:
		res = re.search(e,s)
		if res != None:
			return res.group(1)
		return ""

def connect(link):
	return h.request(link)
#why not add those handler when urlopen to the youtube class????
#TO-DO
def getLinkSize(link):
	return dict(urllib.request.urlopen(link).info())

def getDlink(l, tp, sp, up):
	for rl in l:
		v_type = findByPat(tp, rl) 

		v_sig = findByPat(sp, rl)
		if v_sig.find("&") >= 0:
			v_sig = v_sig[:v_sig.find("&")]
		#print ("sig=", v_sig)

		url = findByPat(up,rl)
		if url.find("&") >= 0:
			url = url[:url.find("&")]
		#print ("url=",url)
		
		if url == "" or v_sig == "":
			print ("Connection problem")
			return False
		
		dlink = urllib.parse.unquote(url + "&signature=" + v_sig)
		#find the size
		sz = int(str(getLinkSize(dlink)['Content-Length']))
		yt.addVideoLink((v_type,urllib.parse.unquote(dlink),sz))
	
	return True

def getDl(link):
	response, content = connect(link)
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

		yt.setDesc(rDesc['content'].encode('utf-8'))
		yt.setImg(rImg['href'])
		res = re.search(r"([?]v=)(.{11})$",rUrl['href'])
		if res != None:
			yt.setId(str(res.group(2)))		
		else:
			print ("hsaha")
		#find Available format
		scriptTag = soup.find_all('script')
		#find the real script
		for e in scriptTag:
			t = e.contents
			if t[0].find("var ytplayer = ytplayer ||") >= 0:
				s = t[0][t[0].find("ytplayer.config = ") + len("ytplayer.config = "):]
				obj = json.loads(s[:-1])
				rformat_list = obj['args']['fmt_list'].split(",")
				#how many format are there
				format_list = [e[:e.find("/")] for e in rformat_list]
				for format in format_list:
					yt.addAvFormat(format)

				#crawl direct link
				rvl = obj['args']['url_encoded_fmt_stream_map'].split(",")
				#res expression group
				type_pat = ['video%2F(.+?)%3B']
				sig_pat = ['sig=(.+)', 'sig=(.+?)&']
				url_pat = ['url=(.+?)&', 'url=(.+)']

				if  not getDlink(rvl, type_pat, sig_pat, url_pat):
					yt.clear()
					return False
				return True
	print ("Link not ready")
	return False

def writeToFile(fn,block):
	with open(fn, "wb") as videofile:
		videofile.write(block)
		yield

percentDisplay = [10.00,20.00,30.00,40.00,50.00,60.00,70.00,80.00,90.00,100.00]

def downloadTo(url,path,name,totalSize,chunk=8192):
	mediaHandler = urllib.request.urlopen(url)
	where = path + name
	progress = 0.0
	f = open(where, "wb")
	print ("Start downloading:")
	aChunk = mediaHandler.read(chunk)
	writeToFile(where,aChunk)
	while progress < totalSize and aChunk:
		f.write(aChunk)
		progress += len(aChunk)
		aChunk = mediaHandler.read(chunk)
		percent = round((progress/totalSize)*100,2)
		if percent in percentDisplay:
			print ("Downloaded : %s%%" % percent)
	f.close()

def fileExist(filename):
	try:
		with open(filename) : pass
	except IOError:
		pass
		return False
	return True
