#main
from YouTube import *
from helper import *
import sys
import os

if __name__ == '__main__':
	argc = len(sys.argv)
	if argc <= 1 or argc > 4:
		print ("Usage : python ytdl.py [youtubelink] [format-OPTIONAL] [quality-OPTIONAL]")
	else:
		if getLink(sys.argv[1]):
			print (yt.getDesc())
			path = os.getcwd() + "\downloaded\\"
			if not os.path.exists(path):
				os.makedirs(path)
			fn = yt.getId()
			print (fn)
			#check if file exist
			if fileExist(path+fn):
				print ("Link is already get")
				print("Please check ",fn ,"for links") 
			else:
				wos = ""
				with open(path+fn,"w+", encoding='utf-8') as file:
					file.write("=============\n")
					file.write("Title: " + yt.getTitle() + "\n")
					file.write("Description: " + yt.getDesc().decode('utf-8') + "\n")
					file.write("Links:==========>\n")
					for format,link in zip(yt.getAvFormat(), yt.getVideoLink()):
						wos = "[" + itag[format] + "]" + "\n" + str(link)
						#print (wos)
						file.write(wos + "\n\n")
					print("Please check ",fn," for links")
					
					if argc == 4:
						video = yt.getVideo(sys.argv[2], sys.argv[3])
					elif argc == 3:
						video = yt.getVideo(sys.argv[2])
					else:
						video = yt.getVideoLink()[0]
					if video:
						url = ""
						vtype = ""
						name = ""
						sz = -1
						l = len(video)
						if l == 1:
							url = str(video[0][0][1])
							vtype = video[0][0][0]
							sz = video[0][0][2]
						else:
							print ("Select one of these video links to download:")
							for i in range(l):
								print (i, " - ", l[i][1])
							print("Please select video:","")
							selected = input()
							if selected > l or selected < 0:
								selected = 0
							url = str(video[selected][0][1])
							vtype = video[selected][0][0]
							sz = video[selected][0][2]
						name = yt.getId() + "." + vtype
						downloadTo(url,path,name,sz)
		else: 
			print ("False")