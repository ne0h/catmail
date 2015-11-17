import sys, glob, os, time

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

	def getPrivateKeys(self, username, password):
		print("Login data send to server: " + username + ", " + password)

		print(self.client.getPrivateKeys(username, password))

	def login(self, username, password):
		print("sessionToken: " + self.client.login(username, password).sessionToken)
