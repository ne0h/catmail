import unittest

from catmailtypes import *
import cryptohelper

class TestCrypto(unittest.TestCase):

	def test_Asym_Crypto_With_Seeded_Keypair(self):
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
	def test_Asym_Crypto_With_Two_Seeded_Keypairs(self):
		seed     = "password"
		msg      = "cryptotexttoencrypt"
		nonce    = cryptohelper.generateNonce()

		keyPair1 = cryptohelper.generateSeededKeyPair(seed)
		keyPair2 = cryptohelper.generateSeededKeyPair(seed)

		c = cryptohelper.encryptAsym(msg, nonce, keyPair1.secretKey, keyPair1.publicKey)
		m = cryptohelper.decryptAsym(c, nonce, keyPair2.secretKey, keyPair2.publicKey)
		
		self.assertEqual(msg, m)

if __name__ == '__main__':
	unittest.main()
