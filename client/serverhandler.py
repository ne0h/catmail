import CatMailService
from ttypes import *

from thrift import Thrift
from thrift.transport import THttpClient
from thrift.transport import TTransport
from thrift.protocol import TJSONProtocol

from constants import ErrorCodes

class ServerHandler():

	def __init__(self, serveraddress="http://localhost:9000/catmail"):
		try:
			transport = THttpClient.THttpClient(serveraddress)
			transport = TTransport.TBufferedTransport(transport)
			protocol = TJSONProtocol.TJSONProtocol(transport)

			self.client = CatMailService.Client(protocol)
			transport.open()

		except Thrift.TException:
			print("text")

	def __sendQuery(self, query, args):
		try:
			return (None, eval("self.client." + query)(*args))
		except Thrift.TException as ex:
			return (ex, None)
		except InternalException as ex:
			return (ErrorCodes.InternalServerError, None)
		except ConnectionRefusedError as ex:
			return (ErrorCodes.ConnectionRefused, None)

	def getPrivateKeys(self, username, password):
		return self.__sendQuery("getPrivateKeys", [username, password])

	def requestLoginChallenge(self, username):
		return self.__sendQuery("requestLoginChallenge", [username])

	def login(self, username, challenge, signature):
		return self.__sendQuery("login", [username, challenge, signature])

	def getContactList(self, username, sessionToken, localVersion):
		return self.__sendQuery("getContactList", [username, sessionToken,
			localVersion])

	def addToContactList(self, username, sessionToken, userToAdd, attributes):
		return self.__sendQuery("addToContactList", [username, sessionToken,
			userToAdd, attributes])
