import binascii, pysodium
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

def sha256(input):
	return pysodium.crypto_hash_sha256(str(input))

def kdf(username, password):
	return pysodium.crypto_pwhash_scryptsalsa208sha256(32, password, sha256(username),
		pysodium.crypto_pwhash_scryptsalsa208sha256_OPSLIMIT_INTERACTIVE,
		pysodium.crypto_pwhash_scryptsalsa208sha256_MEMLIMIT_INTERACTIVE)

def byteHashToString(input):
	import sys
	result = ""
	for i in range(0, len(input)):
		if sys.version_info.major == 3:
			tmp = str(hex(ord(chr(input[i]))))[2:]
		else:
			tmp = str(hex(ord(input[i])))[2:]
		if len(tmp) is 1:
			tmp = "0" + tmp
		result += tmp
	return result

def newClient(username, password):

	passwordHash = kdf(username, password)
	passwordHashForServer = sha256(kdf(username, passwordHash))
	print("Password hash to store at server: " + byteHashToString(passwordHashForServer))

	userKeyPair = generateKeyPair()
	exchangeKeyPair = generateKeyPair()
	seededCryptoKeyPair = generateSeededKeyPair(passwordHash)

	#print(pysodium.crypto_pwhash_scryptsalsa208sha256_SALTBYTES)

"""
Encrypts a message symmetrically. Messages that are type(str) are converted to type(bytes) automatically.
"""
def encryptAead(message, ad, nonce, key):
	if type(message) is str:
		message = str.encode(message)

	return pysodium.crypto_aead_chacha20poly1305_encrypt(message, ad, nonce, key)

"""
Decrypts a message symmetrically. Returns type(bytes).
"""
def decryptAead(cipherText, ad, nonce, key):
	return pysodium.crypto_aead_chacha20poly1305_decrypt(cipherText, ad, nonce, key)
