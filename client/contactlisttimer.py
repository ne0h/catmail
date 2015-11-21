import threading

class ContactListTimer(threading.Thread):

	def __restartTimer(self):
		self.__timer = threading.Timer(1, self.__onTimer)
		self.__timer.start()

	def __onTimer(self):
		print("timer!")
		self.__restartTimer()

	def cancel(self):
		if not self.__timer is None:
			self.__timer.cancel()

	def run(self):
		self.__restartTimer()