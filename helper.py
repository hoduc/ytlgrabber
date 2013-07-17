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
import os



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
	#make download folder if not existed
	if not os.path.exists(os.getcwd() + "\downloaded\\"):
		os.makedirs(os.getcwd() + "\downloaded\\")

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

def getDlink(l, sp, up):
	vl = yt.getAvFormat()
	for (f,rl) in zip(vl, l):
		#v_type = findByPat(tp, rl) 
		v_type = itag[f][1]
		#print (v_type)
		#print (itag[v])
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
		req = urllib.request.urlopen(dlink)
		sz = int(str(dict(req.info())['Content-Length']))
		yt.addVideoLink((v_type,dlink,sz, req))
	return True

def downloadImg(link, to):
	imgreq = urllib.request.urlopen(link)
	downloadTo(link, to, yt.getId() + ".png", int(str((dict(imgreq.info())['Content-Length']))), None, None, 8192, imgreq)

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
		#description
		rDesc = w7Con.find('meta',attrs={'itemprop':'description'})
		yt.setDesc(rDesc['content'].encode('utf-8'))
		#image url
		rImg = w7Con.find('link',attrs={'itemprop':'thumbnailUrl'})
		yt.setImg(rImg['href'])
		
		res = re.search(r"([?]v=)(.{11})$",rUrl['href'])
		if res != None:
			yt.setId(str(res.group(2)))		
		else:
			print ("Wrong link format")
			return False
		#create the folders with the id name
		folder_path = os.getcwd() + "\downloaded\\" + yt.getId() + "\\"
		if not os.path.exists(folder_path):
			os.makedirs(folder_path)

		#download the images
		downloadImg(yt.getImg(), folder_path)
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

				if  not getDlink(rvl, sig_pat, url_pat):
					yt.clear()
					return False
				#write out the link

				return True
	print ("Link not ready")
	return False

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL, QObject


class udpt(QtCore.QThread):
	def __init__(self, p, parent=None):
		super(udpt, self).__init__(parent)
		self.percent = p
	
	trigger = QtCore.pyqtSignal(int, name="changed")	

	def setPercent(self, per):
		self.percent = per

	def run(self):
		#print(self.percent)
		self.trigger.emit(self.percent)
    
percentDisplay = [10.00,20.00,30.00,40.00,50.00,60.00,70.00,80.00,90.00,100.00]

def downloadTo(url,path,name,totalSize,statusGui=None, progressGui=None, chunk=8192, handler=None):
	mediaHandler = handler
	if mediaHandler == None:
		mediaHandler = urllib.request.urlopen(url)
	where = path + name
	#print (where)
	f = open(where, "wb")
	progress = 0.0
	print ("Start downloading:")
	aChunk = mediaHandler.read(chunk)
	percent = 0.0
	
	updateProgressThread = udpt(progress)

	if statusGui != None:
		statusGui.setText("Downloading.....")
	if progressGui != None:
		print("here progressgui")
		updateProgressThread.trigger.connect(progressGui.setValue)
		updateProgressThread.start()
	#writeToFile(where,aChunk)
	while progress < totalSize and aChunk:
		f.write(aChunk)
		progress += len(aChunk)
		aChunk = mediaHandler.read(chunk)
		percent = round((progress/totalSize)*100,2)
		if percent in percentDisplay:
			print ("Downloaded : %s%%" % percent)
			if progressGui != None:
				print("here should print")
				updateProgressThread.trigger.emit(int(percent))
	if statusGui != None:
		statusGui.setText("Ready")
	f.close()

def fileExist(filename):
	try:
		with open(filename) : pass
	except IOError:
		pass
		return False
	return True
