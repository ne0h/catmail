from catmailtypes import *
import cryptohelper

keyPair = cryptohelper.generateSeededKeyPair("test")
print(keyPair.secretKey)
