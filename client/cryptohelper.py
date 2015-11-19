import base64, binascii, pysodium

def generateKeyPair():
	from catmailtypes import KeyPair

	publicKey, secretKey = pysodium.crypto_box_keypair()
	return KeyPair(secretKey, publicKey)

def generateSeededKeyPair(seed):
	from catmailtypes import KeyPair

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

	# generate password hashes
	passwordHash = byteHashToString(kdf(username, password))
	passwordHashForServer = byteHashToString(sha256(byteHashToString(kdf(username, passwordHash))))
	print("Password hash:        " + passwordHashForServer)

	# generate keypairs and nonce that will be stored encrypted on the server
	userKeyPair       = generateKeyPair()
	userKeyPairNonce  = generateNonce()
	exchangeKeyPair   = generateKeyPair()
	exchangePairNonce = generateNonce()

	# encrypt secret keys with before hashed password
	userKeyPair.secretKey = encryptAead(userKeyPair.secretKey, "", userKeyPairNonce, passwordHash)
	userKeyPair.publicKey = userKeyPair.publicKey
	print("UserKeyPair (sk):     " + exportBase64(userKeyPair.secretKey))
	print("UserKeyPair (pk):     " + exportBase64(userKeyPair.publicKey))
	print("UserKeyPairNonce:     " + exportBase64(userKeyPairNonce))

	exchangeKeyPair.secretKey = encryptAead(exchangeKeyPair.secretKey, "", exchangePairNonce, passwordHash)
	exchangeKeyPair.publicKey = exchangeKeyPair.publicKey
	print("ExchangeKeyPair (sk): " + exportBase64(exchangeKeyPair.secretKey))
	print("ExchangeKeyPair (pk): " + exportBase64(exchangeKeyPair.publicKey))
	print("ExchangeKeyPairNonce: " + exportBase64(exchangePairNonce))

def exportBase64(input):
	return str(base64.b64encode(input))[2:-1]

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

def decryptAeadBase64Encoded(cipherText, ad, nonce, key):
	return decryptAead(base64.b64decode(cipherText), ad, base64.b64decode(nonce), key)
	