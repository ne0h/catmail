import random, string
from testclient import TestClient
import cryptohelper

class TestUserCreationAndDeletion(TestClient):

	def __init__(self):
		super().__init__()
		
		# create random user data
		username = "".join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(16)) + "@catmail.de"
		password = "".join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(16))
		
		# create user
		self._client.createUser(username, password)
		print("Created " + username)

if __name__ == '__main__':
	TestUserCreationAndDeletion()
