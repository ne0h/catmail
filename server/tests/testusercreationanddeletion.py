import logging, random, string, unittest
from testclient import TestClient
from constants import ErrorCodes
import cryptohelper

class TestUserCreationAndDeletion(unittest.TestCase):

	def test_userCreationAndDeletion(self):
		testClient = TestClient()

		# create random user data
		username = "".join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(16)) + "@catmail.de"
		password = "".join(random.SystemRandom().choice(string.ascii_lowercase) for _ in range(16))
		
		#
		# CREATION STUFF
		#

		# create user
		(err, result) = testClient._client.createUser(username, password)
		self.assertIsInstance(ErrorCodes.NoError, type(err))
		if err is not ErrorCodes.NoError:
			print("Trying to create new user called %s. Creation failed: %s" % (username, err))
		
		# trying to create same user again
		(err, result) = testClient._client.createUser(username, password)
		self.assertIsInstance(ErrorCodes.UserAlreadyExists, type(err))
		if err is not ErrorCodes.UserAlreadyExists:
			print("Trying to create user with same username. Creation failed: %s" % err)

		#
		# DELETION STUFF
		#

		# log new user in so that he can delete hisself
		(err, result) = testClient._client.login(username, password)
		self.assertIsInstance(ErrorCodes.NoError, type(err))
		#if err is not ErrorCodes.NoError:
		#	print("Failed to login")

		# delete user
		#(err, result) = testClient._client.deleteUser(username, testClient._sessionToken)
		#self.assertIsInstance(ErrorCodes.InvalidSession, type(err))
		#if err is not ErrorCodes.InvalidSession:
		#	print("Deleted %s. Deletion failed: %s" % (username, err))

if __name__ == "__main__":
	unittest.main()
