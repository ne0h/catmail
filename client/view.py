from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ttypes import *
 
class FirstRunForm(QWidget):

	def __init__(self, catMailClient, parent=None):
		super(FirstRunForm, self).__init__(parent)

		self.__catMailClient = catMailClient

		self.__errorLbl = QLabel("")
		usernameLbl = QLabel("Username: ")
		passwordLbl = QLabel("Password: ")
		self.__usernameIpt = QLineEdit()
		self.__passwordIpt = QLineEdit()
		self.__passwordIpt.setEchoMode(QLineEdit.Password)

		self.__submitBtn = QPushButton("Login")
		self.__submitBtn.clicked.connect(self.login)

		layout = QGridLayout()
		layout.addWidget(self.__errorLbl, 0, 0, 1, 0)
		layout.addWidget(usernameLbl, 1, 0)
		layout.addWidget(passwordLbl, 2, 0)
		layout.addWidget(self.__usernameIpt, 1, 1)
		layout.addWidget(self.__passwordIpt, 2, 1)
		layout.addWidget(self.__submitBtn, 3, 1)

		self.setLayout(layout)
		self.setWindowTitle("Welcome to CatMail!")

	def __displayError(self, message):
		self.__errorLbl.setText("<font color='red'>%s</font>" % message)

	def login(self):
		username = self.__usernameIpt.text()
		password = self.__passwordIpt.text()

		ex = self.__catMailClient.login(username, password)
		# no exception -> login successful. close firstrunform and start main form
		if ex is None:
			self.close()

		if type(ex) is InvalidLoginCredentialsException:
			self.__displayError("Error: Wrong login credentials.")

class MainForm(QWidget):

	def __init__(self, catMailClient, parent=None):
		super(MainForm, self).__init__(parent)

		self.__catMailClient = catMailClient

		self.setFixedSize(200, 500)
		self.setWindowTitle("CatMail")
