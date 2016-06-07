import CatMailService
from ttypes import *

from thrift import Thrift
from thrift.transport.THttpClient import THttpClient
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol.TJSONProtocol import TJSONProtocol

from constants import ErrorCodes

class ServerHandler():

	def __init__(self):
		self.__transport		= None
		self.__serveraddress	= None
		self.client				= None

	def setServerAddress(self, serveraddress):
		self.__serveraddress = serveraddress

	def disconnect(self):
		if not self.__transport is None:
			self.__transport.close()
			self.__transport	= None
			self.client			= None

	def connect(self):
		self.disconnect()
		rv = ErrorCodes.NoError
		if self.__serveraddress is None or self.__serveraddress == "":
			return ErrorCodes.ServerNotConfigured
		else:
			try:
				print("server: %s" % self.__serveraddress)
				self.__transport	= THttpClient(self.__serveraddress)
				self.__transport	= TBufferedTransport(self.__transport)
				protocol			= TJSONProtocol(self.__transport)

				self.client			= CatMailService.Client(protocol)
				self.__transport.open()
			except Thrift.TException as e:
				rv = ErrorCodes.ThriftError
		return rv


	def __sendQuery(self, query, args):
		if self.client is None:
			return (ErrorCodes.ServerNotConfigured, None)
		try:
			return (ErrorCodes.NoError, eval("self.client." + query)(*args))
	# TODO don't catch TException while debugging...
	#	except Thrift.TException as ex:
	#		return (ex, None)
		except InternalException as ex:
			return (ErrorCodes.InternalServerError, None)
		except ConnectionRefusedError as ex:
			return (ErrorCodes.ConnectionRefused, None)

	def getPrivateKeys(self, username, password):
		err, resp = (ErrorCodes.NoError, None)
		try:
			err, resp = self.__sendQuery("getPrivateKeys", [username, password])
		except InvalidLoginCredentialsException:
			err = ErrorCodes.LoginCredentialsInvalid
		return (err, resp)


	def requestLoginChallenge(self, username):
		# No additional exceptions.
		return self.__sendQuery("requestLoginChallenge", [username])

	def login(self, username, challenge, signature):
		err, resp = (ErrorCodes.NoError, None)
		try:
			err, resp = self.__sendQuery("login", [username, challenge, signature])
		except InvalidLoginCredentialsException:
			err = ErrorCodes.LoginCredentialsInvalid
		return (err, resp)

	def logout(self, username, sessionToken):
		err, resp = (ErrorCodes.NoError, None)
		try:
			err, resp = self.__sendQuery("logout", [username, sessionToken])
		except InvalidSessionException:
			err = ErrorCodes.InvalidSession
		return (err, resp)

	def getContactList(self, username, sessionToken, localVersion):
		err, resp = (ErrorCodes.NoError, None)
		try:
			err, resp = self.__sendQuery("getContactList",
					[username, sessionToken, localVersion]
				)
		except InvalidSessionException:
			err = ErrorCodes.InvalidSession
		return (err, resp)

	def addToContactList(self, username, sessionToken, userToAdd, attributes):
		err, resp = (ErrorCodes.NoError, None)
		try:
			err, resp = self.__sendQuery("addToContactList",
					[username, sessionToken, userToAdd, attributes]
				)
		except UserDoesNotExistException:
			err = ErrorCodes.UserDoesNotExist
		return (err, resp)

	def createUser(self, username, password, keyData):
		err, resp = (ErrorCodes.NoError, None)
		userKeyPair     = EncryptedKeyPair(keyData[0], keyData[1], keyData[2])
		exchangeKeyPair = EncryptedKeyPair(keyData[3], keyData[4], keyData[5])

		try:
			err, resp = self.__sendQuery("createUser",
					[username, password, userKeyPair,
					exchangeKeyPair])
		except UserAlreadyExistsException:
			err = ErrorCodes.UserAlreadyExists
		return (err, resp)

	def deleteUser(self, username, sessionToken):
		err, resp = (ErrorCodes.NoError, None)
		try:
			err, resp = self.__sendQuery("deleteUser",
					[username, sessionToken])
		except InternalException:
			err = ErrorCodes.InternalServerError
		except InvalidSessionException:
			err = ErrorCodes.InvalidSession
		return (err, resp)

	def createChat(self, username, sessionToken, usersToAdd):
		err, resp = (ErrorCodes.NoError, None)
		try:
			err, resp = self.__sendQuery("createChat",
					[username, sessionToken, usersToAdd])
		except InvalidSessionException:
			err = ErrorCodes.InvalidSession
		except UserDoesNotExistException:
			err = ErrorCodes.UserDoesNotExist
		return (err, resp)
