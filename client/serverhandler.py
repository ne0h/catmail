import CatMailService
from ttypes import *

from thrift import Thrift
from thrift.transport import THttpClient
from thrift.transport import TTransport
from thrift.protocol import TJSONProtocol

class ServerHandler():

	def __init__(self):
		try:
			transport = THttpClient.THttpClient("http://localhost:9000/catmail")
			transport = TTransport.TBufferedTransport(transport)
			protocol = TJSONProtocol.TJSONProtocol(transport)

			self.client = CatMailService.Client(protocol)
			transport.open()

		except Thrift.TException:
			print("text")

	def __sendQuery(self, query, args):
		try:
			return None, eval("self.client." + query)(*args)
		except Thrift.TException as ex:
			return ex, None

	def getPrivateKeys(self, username, password):
		return self.__sendQuery("getPrivateKeys", (username, password))


	def login(self, username, challenge, signature):
		return self.__query("login", (username, challenge, signature))
