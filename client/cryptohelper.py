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

def hash(input, salt):
	return pysodium.crypto_box_SEEDBYTES
