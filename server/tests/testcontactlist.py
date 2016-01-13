from testclient import TestClient

class TestContactList(TestClient):

	def __init__(self):
		super().__init__()

		print(self._client.get_server_handler().getContactList(self._username, self._sessionToken, 0))

if __name__ == "__main__":
	TestContactList()
