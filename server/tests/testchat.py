from testclient import TestClient

class TestChat(TestClient):

	def createChat(self, key, usersToAdd):
		return self._client.get_server_handler().createChat(self._username, self._sessionToken, usersToAdd)

	def __init__(self):
		super().__init__()

		print("keeey", self.createChat([]))

if __name__ == "__main__":
	TestChat()
