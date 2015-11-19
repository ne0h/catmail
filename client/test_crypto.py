import base64, binascii, unittest, sys
curVersion = str(sys.version_info.major) + "." + str(sys.version_info.minor)
sys.path.append("../3rdparty/thrift-build/lib/python" + curVersion
	+ "/site-packages/thrift.egg")
sys.path.append("../3rdparty/thrift-build/lib/python" + curVersion
	+ "/site-packages/six.egg")
sys.path.append("./api/protocol")
sys.path.append("../3rdparty/pysodium-build/lib/python" + curVersion + "/site-packages/pysodium-0.6.8-py"
	+ curVersion + ".egg")

import cryptohelper

class TestCrypto(unittest.TestCase):

	"""
	Tests if seeded keypairs are always equal (with same seed).
	"""
	def test_AsymCryptoWithSeededKeypair(self):
		seed    = "password"
		msg     = "cryptotexttoencrypt"
		nonce   = cryptohelper.generateNonce()
		keyPair = cryptohelper.generateSeededKeyPair(seed)

		c = cryptohelper.encryptAsym(msg, nonce, keyPair.secretKey, keyPair.publicKey)
		m = cryptohelper.decryptAsym(c, nonce, keyPair.secretKey, keyPair.publicKey)
		
		self.assertEqual(msg, m)

	"""
	Makes sure that two differently generated seeded keypairs are compatible
	"""
	def test_AsymCryptoWithTwoSeededKeypairs(self):
		seed     = "password"
		msg      = "cryptotexttoencrypt"
		nonce    = cryptohelper.generateNonce()

		keyPair1 = cryptohelper.generateSeededKeyPair(seed)
		keyPair2 = cryptohelper.generateSeededKeyPair(seed)

		c = cryptohelper.encryptAsym(msg, nonce, keyPair1.secretKey, keyPair1.publicKey)
		m = cryptohelper.decryptAsym(c, nonce, keyPair2.secretKey, keyPair2.publicKey)
		
		self.assertEqual(msg, m)

	"""
	Tests AEAD encryption.
	"""
	def test_aeadWithSeededKeypairs(self):
		msg   = "cryptotexttoencrypt"
		nonce = cryptohelper.generateNonce()
		key   = "topsecretpassword"
		ad = binascii.unhexlify("")

		c = cryptohelper.encryptAead(msg, ad, nonce, key)
		m = cryptohelper.decryptAead(c, ad, nonce, key)

		self.assertEqual(msg, m.decode())

	"""
	Tests if decryption of server stored secretkeys works.
	"""
	def test_encryptKeyPair(self):
		username = "test@catmail.de"
		password = "password"
		passwordHash = cryptohelper.byteHashToString(cryptohelper.kdf(username, password))
		nonce = cryptohelper.generateNonce()
		keypair = cryptohelper.generateKeyPair()

		encrypted = cryptohelper.exportBase64(cryptohelper.encryptAead(keypair.secretKey, "", nonce, passwordHash))
		decrypted = cryptohelper.decryptAead(base64.b64decode(encrypted), "", nonce, passwordHash)
		
		self.assertEqual(keypair.secretKey, decrypted)

if __name__ == '__main__':
	unittest.main()
