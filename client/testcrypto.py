import unittest

from keypair import *
import cryptohelper

class TestCrypto(unittest.TestCase):

	def test_AsymCryptoOneKeypair(self):
		keyPair = cryptohelper.generateKeyPair()

if __name__ == '__main__':
	unittest.main()
