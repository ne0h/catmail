import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import cryptohelper
from view import *
from serverhandler import *

class KeyPair():
	def __init__(self, secretKey, publicKey):
		self.secretKey = secretKey
		self.publicKey = publicKey

class UserContext():
	def __init__(self, username):
		self.username = username

class CatMailClient():

	def __init__(self, nogui=False):

		# start serverhandler to connect to catmail server
		self.serverHandler = ServerHandler()

		# check for local user settings, if nothing found launch firstrunwizard
		
		if not nogui:
			self.startFirstRunForm()

	def startFirstRunForm(self):
		app = QApplication(sys.argv)
		screen = FirstRunForm(self)
		screen.show()
		sys.exit(app.exec_())

	def startMainForm(self):
		print("mainform")

	def login(self, username, password):
		passwordHash = cryptohelper.byteHashToString(cryptohelper.kdf(username, cryptohelper.kdf(username, password)))
		return self.serverHandler.getPrivateKeys(username, passwordHash)
