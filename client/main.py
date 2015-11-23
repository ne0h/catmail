import sys
import argparse
curVersion = str(sys.version_info.major) + "." + str(sys.version_info.minor)
sys.path.append("../3rdparty/thrift-build/lib/python" + curVersion
	+ "/site-packages/thrift.egg")
sys.path.append("../3rdparty/thrift-build/lib/python" + curVersion
	+ "/site-packages/six.egg")
sys.path.append("./api/protocol")
sys.path.append("../3rdparty/pysodium-build/lib/python" + curVersion + "/site-packages/pysodium-0.6.8-py" 
	+ curVersion + ".egg")

from catmailclient import CatMailClient
from catmailclientbackend import CatMailClientBackend
import cryptohelper
 
def setup_argparse():
	newline = '\n'
	parser = argparse.ArgumentParser(description="CatMail Client Application")
	
	parser.add_argument("--new",
			help="Generates all crypto data for a new client",
			nargs=2,
			type=str
		)
	parser.add_argument("--testlogin",
			help="Does a test login",
			nargs=2,
			type=str
		)
	return parser

def __start(nogui=False):
	gui = None
	if not nogui:
		gui = CatMailClient()
	client = CatMailClientBackend(frontend=gui)
	client.start(nogui=nogui)

# Takes command line arguments and does a test login.
def __testlogin(username, password):
	client = CatMailClientBackend()
	client.login(username, password, testlogin=True)

# Generates all crypto data for a new client and prints them.
# This data is to be transfered to catmail server manually.
def __start_fresh(username, password):
	cryptohelper.newClient(sys.argv[2], sys.argv[3])

if __name__ == '__main__':
	args = setup_argparse().parse_args()

	if (args.testlogin):
		__testlogin(*args.testlogin)
	elif (args.new):
		__start_fresh(*args.testlogin)
	else:
	        __start()
