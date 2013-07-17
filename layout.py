# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Ho Duc\Desktop\programming\ytdl\layout.ui'
#
# Created: Tue Jul 16 22:26:14 2013
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from YouTube import *
from helper import *
import sys
import os
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL, QObject

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class GLThread(QtCore.QThread):
    def __init__(self, l, parent=None):
        super(GLThread, self).__init__(parent)
        self.link = l

    trigger = QtCore.pyqtSignal()

    def setLink(self,l):
        self.link = l

    def run(self):
        while not getLink(self.link):
            continue
        self.trigger.emit()

class DVThread(QtCore.QThread):
    def __init__(self, parent=None):
        super(DVThread, self).__init__(parent)
        self.url = ""
        self.path = ""
        self.name = ""
        self.sz = -1
        self.handler = None
        self.statusBar = None
        self.progressBar = None

    trigger = QtCore.pyqtSignal()

    def setVal(self, link, direction, n, tsz, sb, pb, hl):
        self.url = link
        self.path = direction
        self.name = n
        self.sz = tsz
        self.handler = hl
        self.statusBar = sb
        self.progressBar = pb

    def run(self):
        downloadTo(self.url,self.path,self.name,self.sz,self.statusBar, self.progressBar, 8192,self.handler)
        self.trigger.emit()

class Ui_mainWindow(object):
    def __init__(self):
        self.btList = []
        self.threadList = []
          
    def setupUi(self, mainWindow):
        mainWindow.setObjectName(_fromUtf8("mainWindow"))
        mainWindow.resize(554, 400)
        mainWindow.setMinimumSize(QtCore.QSize(554, 400))
        mainWindow.setMaximumSize(QtCore.QSize(554, 400))
        self.horizontalLayoutWidget = QtGui.QWidget(mainWindow)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 551, 51))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.inputLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.inputLayout.setMargin(0)
        self.inputLayout.setObjectName(_fromUtf8("inputLayout"))
        self.inputLink = QtGui.QLineEdit(self.horizontalLayoutWidget)
        self.inputLink.setObjectName(_fromUtf8("inputLink"))
        self.inputLayout.addWidget(self.inputLink)
        self.find = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.find.setObjectName(_fromUtf8("find"))
        self.inputLayout.addWidget(self.find)
        self.inputLayout.connect(self.find, QtCore.SIGNAL('clicked()'), self.fireGetLink)

        self.horizontalLayoutWidget_2 = QtGui.QWidget(mainWindow)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(0, 50, 551, 61))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.avFormatLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.avFormatLayout.setMargin(0)
        self.avFormatLayout.setObjectName(_fromUtf8("avFormatLayout"))
        self.horizontalLayoutWidget_3 = QtGui.QWidget(mainWindow)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(0, 110, 551, 241))
        self.horizontalLayoutWidget_3.setObjectName(_fromUtf8("horizontalLayoutWidget_3"))
        self.infoLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.infoLayout.setMargin(0)
        self.infoLayout.setObjectName(_fromUtf8("infoLayout"))
        self.web = QtWebKit.QWebView(self.horizontalLayoutWidget_3)
        self.web.setUrl(QtCore.QUrl(_fromUtf8("about:blank")))
        self.web.setObjectName(_fromUtf8("web"))
        self.infoLayout.addWidget(self.web)
        self.percent = QtGui.QProgressBar(mainWindow)
        self.percent.setGeometry(QtCore.QRect(0, 350, 551, 31))
        self.percent.setMaximumSize(QtCore.QSize(16777213, 16777215))
        self.percent.setProperty("value", 0)
        self.percent.setObjectName(_fromUtf8("percent"))
        self.status = QtGui.QLabel(mainWindow)
        self.status.setGeometry(QtCore.QRect(0, 380, 551, 21))
        self.status.setText(_fromUtf8(""))
        self.status.setObjectName(_fromUtf8("status"))

        self.glt = GLThread("")

        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(_translate("mainWindow", "YouTubeLinkGrabber", None))
        self.find.setText(_translate("mainWindow", "Find!!!", None))

    def fireGetLink(self):
        self.find.setEnabled(False)
        self.glt.setLink(self.inputLink.text())
        self.glt.trigger.connect(self.downloadImgDone)
        self.glt.start()       
        
    def makeHtml(self):
        print (yt.getId())
        s = "<html><body><p>"
        s += "<img src=" + yt.getId() + ".png" + " width=150 height=150 style=\"float:left'\"/>"
        s += "<b>" + yt.getTitle() + "</b><br>"
        s += yt.getDesc().decode('utf-8')
        s += "</p></body></html>"
        return s

    def downloadImgDone(self):
        print ("Done")
        self.makeAvFormatButton(yt.getAvFormat())
        self.web.setHtml(self.makeHtml(), QtCore.QUrl.fromLocalFile(os.getcwd() + "\downloaded\\" + yt.getId() + "\\"))
        self.find.setEnabled(True)

    def downloadVideoDone(self, t_no):
        print ("Done downloading video")
        [b.setEnabled(True) for (pos,b) in zip(range(len(self.btList)), self.btList) if pos != t_no]

    def makeAvFormatButton(self,l):
        self.btList = []
        self.threadList = []
        for i in range(len(l)):
            self.threadList.append(DVThread())
            self.btList.append(QtGui.QPushButton(self.horizontalLayoutWidget_2))
        for (pos,e) in zip(range(len(l)),l):
            print (pos)
            vi = yt.getVideoLink()[pos]
            path = os.getcwd() + "\downloaded\\" + yt.getId() + "\\"
            name = yt.getId() + "[" + itag[e][0] + "]" + "." + vi[0]

            self.btList[pos].setText(itag[e][0])
            self.btList[pos].setToolTip(itag[e][0])
            self.btList[pos].setEnabled(True)
            
            self.threadList[pos].setVal(vi[1], path, name, vi[2], self.status, self.percent, vi[3])
            self.avFormatLayout.addWidget(self.btList[pos])
            self.avFormatLayout.connect(self.btList[pos], QtCore.SIGNAL('clicked()'),
                lambda tt=self.threadList[pos], tn=pos: self.fireDownload(tt, tn))

    def fireDownload(self,thread_t, thread_no):
        [b.setEnabled(False) for b in self.btList]
        thread_t.trigger.connect(lambda tn=thread_no: self.downloadVideoDone(tn))
        thread_t.start()

from PyQt4 import QtWebKit

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWindow = QtGui.QDialog()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())

