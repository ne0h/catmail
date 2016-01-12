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
		(err, result) = self._client.createUser(username, password)
		if err is None:
			print("Created " + username)
		else:
			print("Creation failed.")
		
		(err, result) = self._client.createUser(username, password)
		if err is None:
			print("Created " + username)
		else:
			print("Creation failed.")

if __name__ == "__main__":
	TestUserCreationAndDeletion()
