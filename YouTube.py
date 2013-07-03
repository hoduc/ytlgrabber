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
	def getVideoLink(self):
		return self.vl
	def getVideo(self, format):
		t = [v for v in self.vl if v[0] == format]
	def getVideo(self, format, quality):
		t = [(v,itag[self.av_format[pos]]) for v,pos in zip(self.vl,range(len(self.vl))) if (v[0].lower() == format.lower() and itag[self.av_format[pos]].split()[0].lower() == quality.lower())]
		return t
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

