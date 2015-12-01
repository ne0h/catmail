import sys
sys.path.append("../../client")
curVersion = str(sys.version_info.major) + "." + str(sys.version_info.minor)
sys.path.append("../../3rdparty/thrift-build/lib/python" + curVersion
	+ "/site-packages/thrift.egg")
sys.path.append("../../3rdparty/thrift-build/lib/python" + curVersion
	+ "/site-packages/six.egg")
sys.path.append("../../client/api/protocol")
sys.path.append("../../3rdparty/pysodium-build/lib/python" + curVersion + "/site-packages/pysodium-0.6.8-py" 
	+ curVersion + ".egg")

from serverhandler import ServerHandler

#
# Parent class for all test cases. Does the login and prepares for further
# tests.
#
class TestClient:

	def __init__(self):
		from config import Config
		from catmailclientbackend import CatMailClientBackend

		# load test settings
		self._config = Config(configDirectory=".")
		username, password = self._config.getLoginCredentials()

		self._client = CatMailClientBackend()
		self._sessionToken = self._client.login(username, password,
			testlogin=True, passwordAlreadyHashed=True)

if __name__ == '__main__':
	TestClient()
