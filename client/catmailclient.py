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
from interfaces import ClientInterface
from constants import ErrorCodes

#TODO make sure there is only one window open at a time

class CatMailClient(ClientInterface):
	def show_dialog(self, title, message, buttons):
		dialog = MessageDialog()
		rv = dialog.show_blocking(
				self.app,
				title,
				message,
				buttons=buttons
			)
		return rv

	"""Displays a warning dialog asking the user if a previously failed action
	should be retried or canceled.

	Returns:
		boolean: true, if the user decides to retry, false otherwise.
	"""
	def show_retry_dialog(self, message):
		btns=[(0, 'Retry'),(1, 'Cancel')]
		rv = self.show_dialog('Retry?', message, btns)
		return (rv == 0)

	def show_error(self, message):
		btns=[(0, 'Ok'), (1, 'Cancel')]
		return self.show_dialog('Error', message, btns)

	def __show_error(self, message):
		self.screen.displayError(message)

	def __cb_login(self, username, password):
		self.logger.debug("Login callback.")
		err = self.backend.login(username, password)
		if err == ErrorCodes.NoError:
			# no error -> login successful.
			# close firstrunform and start main form
			self.screen.close()
			self.cb_success = True
		elif err == ErrorCodes.LoginCredentialsInvalid:
			self.__show_error("Error: Wrong login credentials.")
		else:
			self.__show_error("Error: Unknown error.")

	def first_run(self, loginerror=False):
		#TODO the cb_success thing is hackish... try something else...
		self.cb_success = False
		self.screen = FirstRunForm(self.__cb_login)
		self.screen.show()
		self.app.exec_()
		return self.cb_success
		
	def show(self):
		# check if there is a session token
		#try:
		#	if self.__userContext.sessionToken is None:
		#		self.__startFirstRunForm(self)
		#except AttributeError:
		#	sys.exit()

		#self.app = QApplication(sys.argv)
		self.screen = MainForm(self)
		self.screen.show()
		sys.exit(self.app.exec_())
		
	def addToContactList(self, username):
		print("self.__serverHandler.")

	def init(self, backend):
		self.backend = backend

	def __init__(self, nogui=False):
		self.app = QApplication([]) # QApplication(sys.argv)
		self.backend = None
		self.logger = logging.getLogger("CatMail Client")
		super(CatMailClient, self).__init__()
