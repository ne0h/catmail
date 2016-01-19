from testclient import TestClient

class TestContactList(TestClient):

	def getContactList(self):
		return self._client.get_server_handler().getContactList(self._username, self._sessionToken, 0)

	def addToContactList(self, username):
		return self._client.get_server_handler().addToContactList(self._username, self._sessionToken, username, {})

	def __init__(self):
		super().__init__()

		print(self.addToContactList("max2@catmail.de"))

if __name__ == "__main__":
	TestContactList()
