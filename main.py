#!/usr/bin/env python

from PyQt4 import QtCore, QtGui, QtNetwork
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *
from facebook import Facebook
import sys,os
from FbUtil import *
from ExcelFileReader import *

config_file_path = os.path.join(os.path.expanduser('~'),'fb.ini')

skip_auth = False

class LoginWindow(QtGui.QDialog):
	def __init__(self, parent=None):
		super(LoginWindow, self).__init__(parent)
		self.view = QWebView()
		loginLayout = QtGui.QGridLayout()
		loginLayout.addWidget(self.view,0,0)
		self.setLayout(loginLayout)

class MainWindow(QtGui.QDialog):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)
		self.selectFileButton = QPushButton('Select File',self)
		self.connect(self.selectFileButton,SIGNAL("clicked()"), self._selectFile)
		self.loginButton = QPushButton('Login',self)
		self.connect(self.loginButton,SIGNAL("clicked()"), self._login)

		mainLayout = QtGui.QGridLayout()
		mainLayout.addWidget(self.selectFileButton,0,0)
		mainLayout.addWidget(self.loginButton,0,1)
		self.setLayout(mainLayout)

		self.stage = 0

		self.options = {0:self._loginStage1,
				1:self._loginStage2,
				2:self._loginStage3,
				3:self._loginEnd}

		cf = ConfigFile(config_file_path)

		# get api_key, secret_key and app_Id
		try:
			self.api_key = cf.api_key
			self.secret_key = cf.secret_key
			self.app_Id = cf.app_Id
		except:
			self.api_key = ''
			self.secret_key = ''
			self.app_Id = ''
		# get token and expire time
		try:
			self.token = cf.token
			self.expire = val(cf.expire)
		except:
			self.token = 0
			self.expire = 0

		self.facebook = Facebook(self.api_key, self.secret_key)
		self.facebook.auth.createToken()

	def _selectFile(self):
		self.excelFileName = QFileDialog.getOpenFileName(self,"FileDialog","", "*.xls", "*.xls")
		reader = ExcelFileReader()
		reader.load(self.excelFileName)
		print reader.getHeader()
		print len(reader)
		for r in reader:
			print r

	def _login(self):
		auth_url = self.facebook.get_login_url(next=None,popup=True,canvas=True)
		self.loginWindow = LoginWindow(self)
		self.loginWindow.view.loadFinished.connect(self._stateMachine)
		self.loginWindow.show()
		self.loginWindow.view.load(QUrl(auth_url))
		self.loginButton.hide()
	
	def _stateMachine(self):
		self.options[self.stage]()

	def _loginStage1(self):
		url = str(self.loginWindow.view.url().toString())
		parser = ParseFacebookUrl(url)
		if parser.url != 'https://ssl.facebook.com/desktopapp.php':
			return
		if parser.query.has_key('api_key')==True:
			if parser.query['api_key'] == self.api_key:
				if skip_auth == False:
					self.stage = 1

					extpermurl = self.facebook.get_ext_perm_url(ext_perm='publish_stream', next=None, popup=True)
					self.loginWindow.view.load(QUrl(extpermurl))
				else:
					self.stage = 2
					self._stateMachine()

	def _loginStage2(self):

		self.stage = 2


	def _loginStage3(self):
		self.stage = 3

		self.facebook.auth.getSession()
#		photos = self.facebook.photos.createAlbum('test album2','home','interesting test album')
#		print photos
#		self.facebook.photos.upload(image='C:\\Temp\\facebookupload\\uploadphoto\\logo.gif', aid=photos[u'aid'], caption='good')
				

	def _loginEnd(self):
		self.stage = 4

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	mainWin = MainWindow()
	sys.exit(mainWin.exec_())






