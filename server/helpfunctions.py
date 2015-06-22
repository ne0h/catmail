__author__ = 'adrian'
import base64

def getRandomChallenge(size=64):
    fp = open("/dev/urandom", "rb")
    data = fp.read(64)
    fp.close()
    return base64.encodestring(data).rstrip("\n")
