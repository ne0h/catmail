from PyQt5.QtWidgets import QWidget, QHBoxLayout, QInputDialog
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread, pyqtSignal
from .messages import ConversationsViewManager
from .contactlist import ContactListManager

class MainWindow(QWidget):
	send_message			= pyqtSignal(str, str, name='sendMessage')
	open_chat_intent		= pyqtSignal(str, name='openChatIntent')
	update_contacts_intent		= pyqtSignal(name="update_contacts")
	update_conversations_intent = pyqtSignal(name="update_conversations")
	add_contact_intent			= pyqtSignal(str, name="add_contact")
	add_conversation_intent		= pyqtSignal(str, name="add_conversation")

	def set_contact_list(self, contact_list):
		self.__contact_list.set_contact_list(contact_list)

	def update_contact_list(self):
		self.__contact_list.update_contact_list()

	def add_conversation(self, conversationId, title=None):
		self.__conversationManager.add_conversation(conversationId, title)

	def add_message(self, conversationId, sender, time, message, its_me=False):
		self.__conversationManager.add_message(
				conversationId,
				sender,
				time,
				message,
				its_me
			)

	def __init_ui(self):
		#self.__window.setFixedSize(200, 500)
		self.__window.setWindowTitle("CatMail")

		grid = QHBoxLayout(self)
		grid.addWidget(self.__conversationManager.get_widget())
		grid.addWidget(self.__contact_list.get_widget())

		self.__window.setLayout(grid)
	
	def exit(self):
		pass

	def show(self):
		self.__window.show()
	#	self.__app.exec_()
		self.exit()
	
	def __del__(self):
		#TODO
		pass

	def __send_message(self, message, conversationID):
		self.send_message.emit(message, conversationID)

	def __on_contact_db_cliked(self, cid):
		print("main_window.__on_contact_db_cliked")
		self.open_chat_intent.emit(cid)
		# search conversation
		# not found:
		# 	create
		# open

	def show_add_contact_dialog(self):
		text, status = QInputDialog.getText(
				self.__window,
				"Add Contact",
				"Username:"
			)
		print("Dialog result: %s %s" % (text, status))
		if status and text != '':
			self.add_contact_intent.emit(text)

	def show_add_conversation_dialog(self):
		text, status = QInputDialog.getText(
				self.__window,
				"Add Conversation",
				"Conversation Name:"
			)
		if status and text != '':
			self.add_conversation.emit(text)

	def __connect_signals(self):
		self.__conversationManager.send_message.connect(
			self.__send_message
		)
		self.__contact_list.contact_db_clicked.connect(
			self.__on_contact_db_cliked
		)
		self.__contact_list.add_contact.connect(self.show_add_contact_dialog)
		self.__contact_list.add_conversation.connect(self.show_add_conversation_dialog)

		# Forward
		self.__contact_list.update_contacts.connect(self.update_contacts_intent)
		self.__contact_list.update_conversations.connect(self.update_conversations_intent)

	def __init__(self, catMailClient, app, parent=None):
		super(MainWindow, self).__init__()
		self.__window 			= QWidget(parent)
		self.__app 				= app

		self.__catMailClient 	= catMailClient
		self.__contact_list 	= ContactListManager()
		self.__conversationManager = ConversationsViewManager(self)

		self.__init_ui()
		self.__connect_signals()

