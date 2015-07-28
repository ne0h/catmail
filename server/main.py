from flask import Flask

from flask_jsonrpc import JSONRPC
from XMPP2 import XMPP2


xmpp2 = XMPP2()

app = Flask(__name__)


app.debug=True
jsonrpc = JSONRPC(app,'/')

#TODO Implement authentication the flask rpc way

@jsonrpc.method("requestLoginChallenge(user=str, protocolVersion=str) -> dict", validate=True)
def requestLoginChallenge(user="", protocolVersion=""):
    return xmpp2.requestLoginChallenge(user, protocolVersion)

@jsonrpc.method("login(user=str, clientID=str, loginChallenge=str, loginSignature=str) -> dict", validate=True)
def login(user="", clientID="", loginChallenge="", loginSignature=""):
    return xmpp2.login(user, clientID, loginChallenge, loginSignature)

@jsonrpc.method("logout(sessionCookie=str) -> dict", validate=True)
def logout(sessionCookie=""):
    return xmpp2.logout(sessionCookie)

@jsonrpc.method("getUserPublicKeys(sessionCookie=str, otherUser=str) -> dict", validate=True)
def getUserPublicKeys(sessionCookie="", otherUser=""):
    return xmpp2.getUserPublicKeys(sessionCookie, otherUser)

@jsonrpc.method("setTrust(sessionCookie=str, otherUser=str, keyFingerprint=str, trust=str) -> dict")
def setTrust(sessionCookie="", otherUser="", keyFingerprint="", trust=""):
    raise Exception("Not implemented yet")
    pass

@jsonrpc.method("pollEvents(sessionCookie=str, interest=int) -> dict")
def pollEvents(sessionCookie="", interest=0):
    raise Exception("Not implemented yet")

@jsonrpc.method("getMessageFromLog(sessionCookie=str, chat=int, startMsgId=int, offset=int) -> dict")
def getMessageFromLog(sessionCookie="", chat=0, startMsgId=0, offset=0):
    raise Exception("Not implemented yet")

@jsonrpc.method("getActiveChats(sessionCookie=str) -> dict")
def getActiveChats(sessionCookie=""):
    raise Exception("Not implemented yet")

@jsonrpc.method("getContacts(sessionCookie=str) -> dict")
def getContacts(sessionCookie=""):
    raise Exception("Not implemented yet")

@jsonrpc.method("getContactInfo(sessionCookie=str, otherUser=str) -> dict")
def getContactInfo(sessionCookie="", otherUser=""):
    raise Exception("Not implemented yet")

@jsonrpc.method("addContact(sessionCookie=str, otherUser=str, halloMsg=str) -> dict")
def addContact(sessionCookie=str, otherUser="", halloMsg=""):
    raise Exception("Not implemented yet")

@jsonrpc.method("removeContact(sessionCookie=str, otherUser=str) -> dict")
def removeContact(sessionCookie=str, otherUser=""):
    raise Exception("Not implemented yet")

@jsonrpc.method("blockContact(sessionCookie=str, otherUser=str, silent=bool) -> dict")
def blockContact(sessionCookie="", otherUser="", silent=False):
    raise Exception("Not implemented yet")

@jsonrpc.method("createUser(username=str, password=str, userKey=dict, exchangeKey=str) -> dict") 
def createUser(username, password, userKey, exchangeKey):
    return xmpp2.createUser(username, password, userKey, exchangeKey)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
