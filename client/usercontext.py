class UserContext:

	def __init__(self, username):
		self.username = username

	def setKeyPairs(self, userKeyPair, exchangeKeyPair):
		self.userKeyPair = userKeyPair
		self.exchangeKeyPair = exchangeKeyPair
