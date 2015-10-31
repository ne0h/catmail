import sys
curVersion = str(sys.version_info.major) + "." + str(sys.version_info.minor)
sys.path.append("../3rdparty/pysodium-build/lib/python" + curVersion + "/site-packages/pysodium-0.6.7-py" 
	+ curVersion + ".egg")
import pysodium

from catmailtypes import *

def generateKeyPair():
	publicKey, secretKey = pysodium.crypto_box_keypair()
	return KeyPair(secretKey, publicKey)

def generateSeededKeyPair(seed):
	publicKey, secretKey = pysodium.crypto_box_seed_keypair(seed)
	return KeyPair(secretKey, publicKey)

def generateNonce():
	return pysodium.randombytes(pysodium.crypto_box_NONCEBYTES)

def encryptAsym(msg, nonce, secretKey, publicKey):
	return pysodium.crypto_box_easy(msg, nonce, publicKey, secretKey)

def decryptAsym(c, nonce, secretKey, publicKey):
	return pysodium.crypto_box_open_easy(c, nonce, publicKey, secretKey)
