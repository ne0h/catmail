import base64, configparser, sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import cryptohelper
from view import *
from serverhandler import *

class KeyPair:

	def __init__(self, secretKey, publicKey):
		self.secretKey = secretKey
		self.publicKey = publicKey

class UserContext:

	def __init__(self, username):
		self.username = username

	def setKeyPairs(self, userKeyPair, exchangeKeyPair):
		self.userKeyPair = userKeyPair
		self.exchangeKeyPair = exchangeKeyPair

class CatMailClient:

	def __init__(self, nogui=False):

		# start serverhandler to connect to catmail server
		self.__serverHandler = ServerHandler()

		# check for local user settings, if nothing found launch firstrunwizard
		if not nogui and not Config().exists():
			self.__startFirstRunForm()
		# or login and start main form
		else:
			if not nogui:
				username, password = Config().getLoginCredentials()
				ex = self.login(username, password, passwordAlreadyHashed=True)
				if ex is None:
					self.__startClient()
					self.__startMainForm()
				elif type(ex) is InvalidLoginCredentialsException:
					self.__startFirstRunForm(self)

	def __startFirstRunForm(self, loginerror=False):
		app = QApplication(sys.argv)
		screen = FirstRunForm(self)
		screen.show()
		app.exec_()
		
		self.__startMainForm()

	def __startMainForm(self):

		# check if there is a session token
		try:
			if self.__userContext.sessionToken is None:
				self.__startFirstRunForm(self)
		except AttributeError:
			sys.exit()

		app = QApplication(sys.argv)
		screen = MainForm(self)
		screen.show()
		sys.exit(app.exec_())

	def __startClient(self):

		# start timer for contactlist updates
		print("timer")

	def login(self, username, password, testlogin=False, passwordAlreadyHashed=False):
		if not passwordAlreadyHashed:
			passwordHash = cryptohelper.byteHashToString(cryptohelper.kdf(username, password))
		else:
			passwordHash = password
		loginHash = cryptohelper.byteHashToString(cryptohelper.kdf(username, passwordHash))
		
		ex, res = self.__serverHandler.getPrivateKeys(username, loginHash)
		if ex is not None:
			return ex

		# decrypt secret keys and store them in usercontext
		userKeyPair = KeyPair(cryptohelper.decryptAeadBase64Encoded(res.userKeyPair.encryptedSecretKey, "",
			res.userKeyPair.nonce, passwordHash), base64.b64decode(res.userKeyPair.publicKey))
		exchangeKeyPair = KeyPair(cryptohelper.decryptAeadBase64Encoded(res.exchangeKeyPair.encryptedSecretKey, "",
			res.exchangeKeyPair.nonce, passwordHash), base64.b64decode(res.exchangeKeyPair.publicKey))

		self.__userContext = UserContext(username)
		self.__userContext.setKeyPairs(userKeyPair, exchangeKeyPair)

		# Start challange-response-login. request a login challenge
		ex, res = self.__serverHandler.requestLoginChallenge(username)
		if ex is not None:
			return ex

		# sign this challenge
		signature = cryptohelper.signChallenge(res.challenge, self.__userContext.exchangeKeyPair.secretKey)

		# send the signature to server to log in
		ex, res = self.__serverHandler.login(username, res.challenge, signature)
		if ex is not None:
			return ex

		print("Login successful!\nSessionToken: %s" % (res.sessionToken))

		# store login data if no testlogin
		if not testlogin:
			Config().writeInitialConfig(username, passwordHash)
			self.__userContext.sessionToken = res.sessionToken

			return None

	def addToContactList(self, username):
		print("self.__serverHandler.")

class Config:

	def __init__(self):
		from os.path import expanduser

		self.__configDirectory = expanduser("~") + "/.config/CatMail"
		self.__configFile = self.__configDirectory + "/catmail.ini"

	def exists(self):
		import os

		return os.path.isfile(self.__configFile)

	def writeInitialConfig(self, username, passwordHash):
		from os.path import exists
		import os

		# create containing folder if it does not exist so far
		if not os.path.exists(self.__configDirectory):
			os.makedirs(self.__configDirectory)

		config = configparser.ConfigParser()
		config.add_section("CatMail")
		config.set("CatMail", "username", username)
		config.set("CatMail", "password", passwordHash)

		configFile = open(self.__configFile, "w")
		config.write(configFile)
		configFile.close()

	def getLoginCredentials(self):
		config = configparser.ConfigParser()
		config.read(self.__configFile)

		return config.get("CatMail", "username"), config.get("CatMail", "password")
