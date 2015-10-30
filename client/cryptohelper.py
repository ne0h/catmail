import sys
curVersion = str(sys.version_info.major) + "." + str(sys.version_info.minor)
sys.path.append("../3rdparty/pysodium-build/lib/python" + curVersion + "/site-packages/pysodium-0.6.7-py" 
	+ curVersion + ".egg")
import pysodium

from keypair import *

def generateSeededKeyPair(seed):
	publicKey, secretKey = pysodium.crypto_box_keypair()
	return KeyPair(secretKey, publicKey)
