import base64, sys, threading
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import logging

import cryptohelper
from view import *
from serverhandler import ServerHandler
from config import Config
from keypair import KeyPair
from usercontext import UserContext
from contactlisttimer import ContactListTimer
from interfaces import ClientBackend, ClientInterface
from constants import ErrorCodes
from atomic_lists import ContactList

class CatMailClientBackend(ClientBackend):

	def get_server_handler(self):
		return self.__serverHandler

	def __init_config(self):
		success = False
		self.__config = Config()
		if self.__config.exists():
			self.__logger.debug("Config exists, using it.")
			success = True
		else:
			self.__logger.debug("No config found, creating one.")
			self.__config.init()
		return success

	def __try_login(self):
		username, password = self.__config.getLoginCredentials()
		logged_in = self.login(
				username,
				password,
				passwordAlreadyHashed=True
			)
		return logged_in

	def __init_gui(self):
		if self.__frontend is None \
				or not isinstance(self.__frontend, ClientInterface):
			raise RuntimeError("Cannot init GUI if none is configured")

		self.__frontend.init(self)

	def __get_message(self, error):
		message = "Error."
		if error == ErrorCodes.LoginFailed:
			message = "Login Failed."
		elif error == ErrorCodes.ConnectionRefused:
			message = "Connection refused by server."
		return message

	# TODO join all these __show_foo methods into one + convenience methods
	def __show_error(self, error, nogui):
		rv = None
		message = self.__get_message(error)

		if (nogui):
			print(message)
		if not nogui and not self.__frontend is None:
			rv = self.__frontend.show_error(message)
		return rv
	
	def __show_retry_dialog(self, error, nogui):
		rv = None
		message = self.__get_message(errro)
	
		if (nogui):
			print(message)
		if not nogui and not self.__frontend is None:
			rv = relf.__frontend.show_retry_dialog(message)
		return rv

	def __show_retry_or_new_credentials(self, error, nogui):
		rv = None
		message = self.__get_message(error)
		btns = [(0, 'Retry'), (1, 'Change Credentials'), (2, 'Cancel')]
		
		if (nogui):
			print(message)
		if not nogui and not self.__frontend is None:
			rv = self.__frontend.show_dialog(
					'Login Failed.',
					message,
					btns
					)
		return rv

	def __login_loop(self, nogui, loginerror):
		retry = True
		canceled = False
		err = ErrorCodes.LoginFailed if loginerror else ErrorCodes.NoError
		while retry and not canceled:
			if err == ErrorCodes.NoError:
			    err = self.__try_login()
			else:
			    err = ErrorCodes.NoError \
				if self.__frontend.first_run(loginerror=loginerror) \
				else ErrorCodes.LoginFailed
			if err != ErrorCodes.NoError:
				success = False
				self.__logger.debug("There is a config, but we can't log in...")
				c = self.__show_retry_or_new_credentials(err, nogui)
				if c == 2:
					canceled = True
					retry = False
				elif c == 1:
					canceled = self.__frontend.first_run(loginerror=loginerror)
			else:
				retry = False
		return canceled

	def get_contact_list(self):
		return self.__contact_list

	def update_contacts(self, callback):
		error, response = self.__serverHandler.getContactList(
				self.__userContext.username,
				self.__userContext.sessionToken, 
				self.__contact_list_revision
			)
		if (error == ErrorCodes.NoError and not callback is None):
			self.__contact_list.update_contacts(response)
			print("ContactList update callback")
			callback(self.__contact_list)

	def __show_main_window(self):
		self.__frontend.show()

		# self.update_contact_list()
		# self.__frontend.update_contacts(self.get_contact_list)
		contacts = self.get_contact_list()
		print(contacts)

		# TODO remove when threaded, debug only!
		# NOTE: The following call is blocking!
		self.__frontend.wait()

	def start(self, nogui=False):
		success = self.__init_config()
		err = ErrorCodes.NoError
		canceled = False
		self.__logger.debug("Background service started.")

		if not nogui:
			self.__init_gui()

		canceled = self.__login_loop(nogui, (not success))

		if not canceled:
			self.__show_main_window()
		else:
			self.__logger.info("Exiting...")

	def __start_pull_timer(self):
		# start timer for contactlist updates
		ContactListTimer().start()
		
	def login(self,
			username,
			password,
			testlogin=False,
			passwordAlreadyHashed=False
		):
		if not passwordAlreadyHashed:
			passwordHash = cryptohelper.byteHashToString(
					cryptohelper.kdf(username, password)
				)
		else:
			passwordHash = password
		loginHash = cryptohelper.byteHashToString(
				cryptohelper.kdf(username, passwordHash)
			)
		
		err, res = self.__serverHandler.getPrivateKeys(username, loginHash)
		if err != ErrorCodes.NoError:
			self.__logger.error("Failed to get private keys: %s" % err)
			return err

		# decrypt secret keys and store them in usercontext
		userKeyPair = KeyPair(
				cryptohelper.decryptAeadBase64Encoded(
					res.userKeyPair.encryptedSecretKey, "",
					res.userKeyPair.nonce, passwordHash
				),
				base64.b64decode(res.userKeyPair.publicKey)
			)
		exchangeKeyPair = KeyPair(
				cryptohelper.decryptAeadBase64Encoded(
					res.exchangeKeyPair.encryptedSecretKey, "",
					res.exchangeKeyPair.nonce, passwordHash
				),
				base64.b64decode(res.exchangeKeyPair.publicKey)
			)

		self.__userContext = UserContext(username)
		self.__userContext.setKeyPairs(userKeyPair, exchangeKeyPair)

		# Start challange-response-login. request a login challenge
		err, res = self.__serverHandler.requestLoginChallenge(username)
		if err != ErrorCodes.NoError:
			self.__logger.error("Failed to request challenge: %s" % err)
			return err

		# sign this challenge
		signature = cryptohelper.signChallenge(
				res.challenge,
				self.__userContext.exchangeKeyPair.secretKey
			)

		# send the signature to server to log in
		err, res = self.__serverHandler.login(username, res.challenge, signature)
		if err != ErrorCodes.NoError:
			self.__logger.error("Failed to login: %s" % err)
			return err

		print("Login successful!\nSessionToken: %s" % (res.sessionToken))

		# store login data if no testlogin
		if not testlogin:
			Config().writeInitialConfig(username, passwordHash)
			self.__userContext.sessionToken = res.sessionToken

			return ErrorCodes.NoError

		# if testlogin, return sessionToken
		else:
			return res.sessionToken

	def addToContactList(self, username):
		# TODO
		pass

	def createUser(self, username, password):
		return self.__serverHandler.createUser(username, password,
			cryptohelper.newUser(username, password))

	def __init__(self, frontend=None):
		super(CatMailClientBackend, self).__init__()
		# start serverhandler to connect to catmail server
		self.__logger 			= logging.getLogger("CatMail Client")
		self.__logger.setLevel(logging.DEBUG)
		# create console handler and set level to debug
		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)
		# create formatter
		formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(name)s: %(message)s')
		# add formatter to ch
		ch.setFormatter(formatter)
		# add ch to logger
		self.__logger.addHandler(ch)

		self.__contact_list 	= ContactList()
		self.__contact_list_revision = 0
		self.__serverHandler 	= ServerHandler()
		self.__frontend 		= frontend
		self.__config 			= None

