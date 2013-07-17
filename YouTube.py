#Tag : Dictionary of video format and its itag
itag = {
	"5"   : ("240p_FLV", "flv"),
	"6"   : ("270p_FLV", "flv"),
	"13"  : ("N/A_3GP", "3gpp"),
	"17"  : ("144p_3GP", "3gpp"),
	"18"  : ("270p_MP4", "mp4"),
	"22"  : ("720p_MP4", "mp4"),
	"34"  : ("360p_FLV", "flv"),
	"35"  : ("480p_FLV", "flv"),
	"36"  : ("240p_3GP", "3gpp"),
	"37"  : ("1080p_MP4", "mp4"),
	"38"  : ("3072p_MP4", "mp4"),
	"43"  : ("360p_WebM", "webm"),
	"44"  : ("480p_WebM", "webm"),
	"45"  : ("720p_WebM", "webm"),
	"46"  : ("1080p_WebM", "webm"),
	"82"  : ("360p_MP4", "mp4"),
	"83"  : ("240p_MP4", "mp4"),
	"84"  : ("720p_MP4", "mp4"),
	"85"  : ("520p_MP4", "mp4"),
	"100" : ("360p_MP4", "mp4"),
	"101" : ("360p_MP4", "mp4"),
	"102" : ("720p_WebM", "webm"),
	"120" : ("720p_FLV", "flv")
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
	#tuple (format, direct link, size, urlhandler)
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

