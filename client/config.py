import configparser
import os
from os.path import expanduser

class Config:
	_SECTION="CatMail"

	def __init__(self, configDirectory=expanduser("~") + "/.config/CatMail"):
		self.__configDirectory = configDirectory
		self.__configFile = self.__configDirectory + "/catmail.ini"

	def exists(self):
		return os.path.isfile(self.__configFile)

	def writeInitialConfig(self, username, passwordHash,
			server="http://localhost", port=9000, subdir="catmail"):

		print("fooooo")
		# create containing folder if it does not exist so far
		if not os.path.exists(self.__configDirectory):
			os.makedirs(self.__configDirectory)

		config = configparser.ConfigParser()
		config.add_section(self._SECTION)
		config.set(self._SECTION, "username", username)
		config.set(self._SECTION, "password", passwordHash)
		config.set(self._SECTION, "server", server)
		config.set(self._SECTION, "port", str(port))
		config.set(self._SECTION, "subdir", subdir)

		configFile = open(self.__configFile, "w")
		config.write(configFile)
		configFile.close()

	def init(self, server="http://localhost", port=9000, subdir="catmail"):
		config = configparser.ConfigParser()
		config.add_section(self._SECTION)
		config.set(self._SECTION, "server", server)
		config.set(self._SECTION, "port", str(port))
		config.set(self._SECTION, "subdir", subdir)
		configFile = open(self.__configFile, "w")
		config.write(configFile)
		configFile.close()

	def getServerAddress(self):
		config = configparser.ConfigParser()
		config.read(self.__configFile)
		server	= config.get(self._SECTION, "server")
		port	= config.get(self._SECTION, "port")
		subdir	= config.get(self._SECTION, "subdir")
		return server \
			+ (':' + port if not port is None and port != '' else '') \
			+ ('/' if not subdir is None and subdir[0] != '/' else '') \
			+ subdir

	def getLoginCredentials(self):
		config = configparser.ConfigParser()
		config.read(self.__configFile)

		rv = (None, None)
		if config.has_option(self._SECTION, "username") \
			and config.has_option(self._SECTION, "password"):
		    rv = (config.get(self._SECTION, "username"),
			config.get(self._SECTION, "password"))
		return rv
