#!/usr/bin/env python

from PyQt4 import QtCore, QtGui, QtNetwork
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from facebook import Facebook
from time import gmtime
import os,sys,tempfile,calendar,datetime,re

app_Id_key = 'app_Id'
api_key_key = 'api_key'
secret_key_key = 'secret_key'
token_key = 'token'
expire_key = 'expire'
last_login_key = 'last_login'

config_file = 'fb.ini'

class FacebookLoginUI(QtGui.QDialog):
    def __init__(self, app_Id, parent=None):
        super(FacebookLoginUI, self).__init__(parent)
	self.view = QWebView()
	url = 'https://graph.facebook.com/oauth/authorize?client_id='+app_Id+'&redirect_uri=http://www.facebook.com/connect/login_success.html&type=user_agent&display=popup'
	print url
	self.view.load(QUrl(url))
	self.view.loadFinished.connect(self._loadFinished)

	mainLayout = QtGui.QGridLayout()
	mainLayout.addWidget(self.view,0,0)
	self.setLayout(mainLayout)

        self.setWindowTitle("Facebook Login")

    def _loadFinished(self):
	print "_loadFinished"
	url = str(self.view.url().toString())
	pairdel = str(self.view.url().queryPairDelimiter())
	valdel = str(self.view.url().queryValueDelimiter())
	urllist = url.partition('#')
	if urllist[0] == 'http://www.facebook.com/connect/login_success.html':
		rep = urllist[2]
		pair = rep.split(pairdel)
		for p in pair:
			v = p.split(valdel)
			if v[0]=='access_token':
				self.token = v[1]
			if v[0]=='expires_in':
				self.expire = int(v[1])
		self.view = None
		self.hide()

    def getToken(self):
	return self.token

    def getExpire(self):
	return self.expire

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    ret = 0

    # read config file
    configfile = os.path.join(os.path.dirname(__file__),'fb.ini')
    para = {}
    if os.path.exists(configfile):
        f = open(configfile,'r')
        lines = f.readlines()
        for line in lines:
	    matchequal = re.match(r'^\s*(\S+)\s*=\s*(\S+)',line)
	    if matchequal:
		para[matchequal.group(1)] = matchequal.group(2)
        f.close()

    # read token file
    keyfile = os.path.join(tempfile.gettempdir(),'fb.key')
    if os.path.exists(keyfile):
        f = open(keyfile,'r')
        lines = f.readlines()
        for line in lines:
	    matchequal = re.match(r'^\s*(\S+)\s*=\s*(\S+)',line)
	    if matchequal:
		para[matchequal.group(1)] = matchequal.group(2)
        f.close()

    # try login
    if not(para.has_key(token_key)) or para[token_key] == '':
	    if para.has_key(app_Id_key) and para[app_Id_key] != '':
		    facebookloginui = FacebookLoginUI(para[app_Id_key])
		    facebookloginui.show()
		    ret = facebookloginui.exec_()
	    else:
		    print 'no app_Id, can\'t login'

    sys.exit(ret)

