import binascii, unittest, sys
curVersion = str(sys.version_info.major) + "." + str(sys.version_info.minor)
sys.path.append("../3rdparty/thrift-build/lib/python" + curVersion
	+ "/site-packages/thrift.egg")
sys.path.append("../3rdparty/thrift-build/lib/python" + curVersion
	+ "/site-packages/six.egg")
sys.path.append("./api/protocol")
sys.path.append("../3rdparty/pysodium-build/lib/python" + curVersion + "/site-packages/pysodium-0.6.7-py" 
	+ curVersion + ".egg")

from catmailtypes import *
import cryptohelper

class TestCrypto(unittest.TestCase):

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

	def test_aeadWithSeededKeypairs(self):
		msg   = "cryptotexttoencrypt"
		nonce = cryptohelper.generateNonce()
		key   = "topsecretpassword"
		ad = binascii.unhexlify("")

		c = cryptohelper.encryptAead(msg, ad, nonce, key)
		m = cryptohelper.decryptAead(c, ad, nonce, key)

		self.assertEqual(msg, m.decode())

if __name__ == '__main__':
	unittest.main()
