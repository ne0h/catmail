import sys, glob, os, time
sys.path.append("/Users/ne0h/Projekte/catmail/3rdparty/thrift-build/lib/python3.5/site-packages/thrift.egg")
sys.path.append("/Users/ne0h/Projekte/catmail/3rdparty/thrift-build/lib/python3.5/site-packages/six.egg")
sys.path.append("/Users/ne0h/Projekte/catmail/client/api/protocol")

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

	def login(self, username, password):
		print("sessionToken: " + self.client.login(username, password).sessionToken)
