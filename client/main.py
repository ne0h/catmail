from keypair import *
import cryptohelper

keyPair = cryptohelper.generateKeyPair()
print keyPair.secretKey
