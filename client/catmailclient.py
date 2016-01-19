import base64, sys, threading
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import logging

from view import *
from views.mainwindow import MainWindow
from config import Config
from keypair import KeyPair
from usercontext import UserContext
from contactlisttimer import ContactListTimer
from interfaces import ClientInterface
from constants import ErrorCodes
from contact import CatMailContact

# TODO make sure there is only one window open at a time

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
		#TODO make this method useable for main_window, too
		self.login_dialog.displayError(message)

	def __cb_login(self, username, password):
		self.logger.debug("Login callback.")
		err = self.backend.login(username, password)
		if err == ErrorCodes.NoError:
			# no error -> login successful.
			# close firstrunform and start main form
			self.login_dialog.close()
			self.cb_success = True
		elif err == ErrorCodes.LoginCredentialsInvalid:
			self.__show_error("Error: Wrong login credentials.")
		else:
			self.__show_error("Error: Unknown error.")

	def __on_start_conversation_intent(self, cid):
		new = None
		if not self.conversations_list is None:
			for conversation in self.conversations_list:
				if conversation.is_private() \
						and conversation.is_participant(cid) \
				:
					# TODO careful, locking!!
					new = conversation
					break

	def first_run(self, loginerror=False):
		#TODO the cb_success thing is hackish... try something else...
		self.cb_success = False
		self.login_dialog = FirstRunForm(self.__cb_login)
		self.login_dialog.show()
		self.app.exec_()
		return self.cb_success

	def __on_contacts_updated(self, contacts):
		self.contact_list = contacts
		self.main_window.set_contact_list(contacts)
		self.main_window.update_contacts()

	def update_conversations(self, conversations):
		self.conversations_list = conversations

	def __on_send_message(self, message, conversationID):
	    print("conversation: %s, message: '%s'" %
				(conversationID, message))
		
	def show(self):
		#TODO...
		# check if there is a session token
		#try:
		#	if self.__userContext.sessionToken is None:
		#		self.__startFirstRunForm(self)
		#except AttributeError:
		#	sys.exit()

		#self.app = QApplication(sys.argv)
		self.main_window = MainWindow(self, self.app)
		self.backend.update_contacts(self.__on_contacts_updated)
		# self.__connect_mani_window_signals()
		self.main_window.show()

	def add_conversation(self, conversationId, title=None):
		self.main_window.add_conversation(conversationId, title)

	def add_message(self, conversationId, sender, time, message, its_me=False):
		self.main_window.add_message(conversationId, sender, time,
                        message, its_me)

	#TODO remove when threaded, debug only!
	def wait(self):
		sys.exit(self.app.exec_())
		
	def addToContactList(self, username):
		print("self.__serverHandler.")

	def init(self, backend):
		self.backend = backend

	def __init__(self, nogui=False):
		self.app = QApplication([]) # QApplication(sys.argv)
		self.backend = None
		self.logger = logging.getLogger("CatMail Client")
		self.contact_list 		= None
		self.conversations_list = None
		super(CatMailClient, self).__init__()
