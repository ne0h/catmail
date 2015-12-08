from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QPushButton

class DialogBtn(QPushButton):
	def __click_cb(self):
		if not self.__callback is None:
			self.__callback(self.__idx)

	def __init__(self, b, idx, parent, callback=None):
		super(DialogBtn, self).__init__(b, parent)
		self.__idx = idx
		self.__callback = callback
		self.clicked.connect(self.__click_cb)

class MessageDialog(QDialog):
	def __btn_click_callback(self, idx):
		self.__return = idx
		self.close()

	def show_blocking(self, app, title, message, buttons=[(0, 'Ok'), (1, 'Cancel')]):
		self.setWindowTitle(title)
		grid = QGridLayout(self)

		lMessage = QLabel(self)
		lMessage.setText(message)
		lMessage.resize(lMessage.sizeHint())
		grid.addWidget(lMessage, 0, 0, 1, len(buttons))

		btns = []
		self.__return = None
		
		for i, b in enumerate(buttons):
			btn = DialogBtn(b[1], b[0], self, self.__btn_click_callback)
			grid.addWidget(btn, 1, i)
		
		self.show()
		app.exec_()
		return self.__return

	def __init__(self):
		super(MessageDialog, self).__init__()
 
class FirstRunForm(QWidget):
	def __setup_gui(self):
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

	def __init__(self, callback, parent=None):
		super(FirstRunForm, self).__init__(parent)
		self.__login_callback = callback

		self.__setup_gui()

	def displayError(self, message):
		self.__errorLbl.setText("<font color='red'>%s</font>" % message)

	def login(self):
		username = self.__usernameIpt.text()
		password = self.__passwordIpt.text()
		print("login")

		self.__login_callback(username, password)
