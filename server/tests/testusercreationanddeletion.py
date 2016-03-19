import random, string
from testclient import TestClient
from constants import ErrorCodes
import cryptohelper

class TestUserCreationAndDeletion(TestClient):

	def __init__(self):
		super().__init__()
		
		# create random user data
		username = "".join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(16)) + "@catmail.de"
		password = "".join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(16))
		
		# create user
		print("Trying to create new user called %s" % username)
		(err, result) = self._client.createUser(username, password)
		if err is ErrorCodes.NoError:
			print("Created %s" % username)
		else:
			print("Creation failed: %s" % err)
		
		print("Trying to create user with same username")
		(err, result) = self._client.createUser(username, password)
		if err is ErrorCodes.NoError:
			print("Created %s" % username)
		else:
			print("Creation failed: %s" % err)

		(err, result) = self._client.deleteUser(username, self._sessionToken)
		if err is ErrorCodes.NoError:
			print("Deleted %s" % username)
		else:
			print("Deletion failed: %s" % err)

if __name__ == "__main__":
	TestUserCreationAndDeletion()
