import sys
curVersion = str(sys.version_info.major) + "." + str(sys.version_info.minor)
sys.path.append("../3rdparty/thrift-build/lib/python" + curVersion
	+ "/site-packages/thrift.egg")
sys.path.append("../3rdparty/thrift-build/lib/python" + curVersion
	+ "/site-packages/six.egg")
sys.path.append("./api/protocol")
sys.path.append("../3rdparty/pysodium-build/lib/python" + curVersion + "/site-packages/pysodium-0.6.8-py" 
	+ curVersion + ".egg")

from catmailtypes import *
import cryptohelper
 
if __name__ == '__main__':

	if len(sys.argv) == 1:
		CatMailClient()
	else:
		cmd = sys.argv[1]

		if (cmd == "help"):
			print("Usage:")
			print("python main.py help                         		Prints this information")
			print("python main.py new username password        		Generates all crypto data for a new client")
			print("python main.py testlogin username password       Does a test login")

		# Generates all crypto data for a new client and prints them.
		# This data is to be transfered to catmail server manually.
		elif cmd == "new":
			cryptohelper.newClient(sys.argv[2], sys.argv[3])

		# Takes command line arguments and does a test login.
		elif cmd == "testlogin":
			CatMailClient(nogui=True).login(sys.argv[2], sys.argv[3], testlogin=True)

		else:
			print("Command not known.")
	