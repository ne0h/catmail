import sys, base64
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
		passwordHash = cryptohelper.byteHashToString(cryptohelper.kdf(username, password))
		loginHash = cryptohelper.byteHashToString(cryptohelper.kdf(username, passwordHash))
		
		ex, response = self.serverHandler.getPrivateKeys(username, loginHash)
		if ex is not None:
			print(type(ex).__name__)
			return ex, None

		# decrypt secret keys and store them in usercontext
		userKeyPair = KeyPair(cryptohelper.decryptAeadBase64Encoded(response.userKeyPair.encryptedSecretKey, "",
			response.userKeyPair.nonce, passwordHash), base64.b64decode(response.userKeyPair.publicKey))
		exchangeKeyPair = KeyPair(cryptohelper.decryptAeadBase64Encoded(response.exchangeKeyPair.encryptedSecretKey, "",
			response.exchangeKeyPair.nonce, passwordHash), base64.b64decode(response.exchangeKeyPair.publicKey))

		self.userContext = UserContext(username)
		self.userContext.setKeyPairs(userKeyPair, exchangeKeyPair)

		# Start challange-response-login. request a login challenge
		ex, response = self.serverHandler.requestLoginChallenge(username)
		if ex is not None:
			print(type(ex).__name__)
			return ex, None

		# sign this challenge
		signature = cryptohelper.signChallenge(response.challenge, self.userContext.exchangeKeyPair.secretKey)

		# send the signature to server to log in
		ex, response = self.serverHandler.login(username, response.challenge, signature)
		if ex is not None:
			print(type(ex).__name__)
			return ex, None

		print("Login successful!\nSessionToken is: %s" % (response.sessionToken))
