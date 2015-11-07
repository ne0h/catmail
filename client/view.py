from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
 
class FirstRunForm(QWidget):

	def __init__(self, catMailClient, parent=None):
		super(FirstRunForm, self).__init__(parent)

		self.catMailClient = catMailClient

		usernameLbl = QLabel("Username: ")
		passwordLbl = QLabel("Password: ")
		self.usernameIpt = QLineEdit()
		self.passwordIpt = QLineEdit()

		self.submitBtn = QPushButton("Login")
		self.submitBtn.clicked.connect(self.login)

		layout = QGridLayout()
		layout.addWidget(usernameLbl, 0, 0)
		layout.addWidget(passwordLbl, 1, 0)
		layout.addWidget(self.usernameIpt, 0, 1)
		layout.addWidget(self.passwordIpt, 1, 1)
		layout.addWidget(self.submitBtn, 2, 1)

		self.setLayout(layout)
		self.setWindowTitle("Welcome to CatMail!")

	def login(self):
		username = self.usernameIpt.text()
		password = self.passwordIpt.text()

		sessionToken = self.catMailClient.login(username, password)
		print(sessionToken)
