import configparser
from os.path import expanduser

class Config:

	def __init__(self, configDirectory=expanduser("~") + "/.config/CatMail"):
		self.__configDirectory = configDirectory
		self.__configFile = self.__configDirectory + "/catmail.ini"

	def exists(self):
		import os

		return os.path.isfile(self.__configFile)

	def writeInitialConfig(self, username, passwordHash):
		from os.path import exists
		import os

		# create containing folder if it does not exist so far
		if not os.path.exists(self.__configDirectory):
			os.makedirs(self.__configDirectory)

		config = configparser.ConfigParser()
		config.add_section("CatMail")
		config.set("CatMail", "username", username)
		config.set("CatMail", "password", passwordHash)

		configFile = open(self.__configFile, "w")
		config.write(configFile)
		configFile.close()

	def init(self):
		pass

	def getLoginCredentials(self):
		config = configparser.ConfigParser()
		config.read(self.__configFile)

		return config.get("CatMail", "username"), config.get("CatMail", "password")
