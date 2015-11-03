import sys

from catmailtypes import *
import cryptohelper

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
 
class Form(QWidget):
	def __init__(self, parent=None):
		super(Form, self).__init__(parent)

 
if __name__ == '__main__':
	app = QApplication(sys.argv)
	screen = Form()
	screen.show()
	sys.exit(app.exec_())