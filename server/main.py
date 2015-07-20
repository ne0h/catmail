from flask import Flask

from flask_jsonrpc import JSONRPC
from XMPP2 import XMPP2


xmpp2 = XMPP2()

app = Flask(__name__)


app.debug=True
jsonrpc = JSONRPC(app, '/api')

#TODO Implement authentication the flask rpc way

@jsonrpc.method("RequestLoginChallenge(user=str, protocolVersion=str) -> dict", validate=True)
def RequestLoginChallenge(user="", protocolVersion=""):
    return xmpp2.RequestLoginChallenge(user, protocolVersion)

@jsonrpc.method("Login(user=str, clientID=str, loginChallenge=str, loginSignature=str) -> dict", validate=True)
def Login(user="", clientID="", loginChallenge="", loginSignature=""):
    return xmpp2.Login(user, clientID, loginChallenge, loginSignature)

@jsonrpc.method("Logout(sessionCookie=str) -> dict", validate=True)
def Logout(sessionCookie=""):
    return xmpp2.Logout(sessionCookie)

@jsonrpc.method("GetUserPublicKeys(sessionCookie=str, otherUser=str) -> dict", validate=True)
def GetUserPublicKeys(sessionCookie="", otherUser=""):
    return xmpp2.GetUserPublicKeys(sessionCookie, otherUser)
@jsonrpc.method("SetTrust(sessionCookie=str, otherUser=str, keyFingerprint=str, trust=str) -> dict")
def SetTrust(sessionCookie="", otherUser="", keyFingerprint="", trust=""):
    raise Exception("Not implemented yet")
    pass

@jsonrpc.method("PollEvents(sessionCookie=str, interest=int) -> dict")
def PollEvents(sessionCookie="", interest=0):
    raise Exception("Not implemented yet")

@jsonrpc.method("GetMessageFromLog(sessionCookie=str, chat=int, startMsgId=int, offset=int) -> dict")
def GetMessageFromLog(sessionCookie="", chat=0, startMsgId=0, offset=0):
    raise Exception("Not implemented yet")

@jsonrpc.method("GetActiveChats(sessionCookie=str) -> dict")
def GetActiveChats(sessionCookie=""):
    raise Exception("Not implemented yet")

@jsonrpc.method("GetContacts(sessionCookie=str) -> dict")
def GetContacts(sessionCookie=""):
    raise Exception("Not implemented yet")

@jsonrpc.method("GetContactInfo(sessionCookie=str, otherUser=str) -> dict")
def GetContactInfo(sessionCookie="", otherUser=""):
    raise Exception("Not implemented yet")

@jsonrpc.method("AddContact(sessionCookie=str, otherUser=str, halloMsg=str) -> dict")
def AddContact(sessionCookie=str, otherUser="", halloMsg=""):
    raise Exception("Not implemented yet")

@jsonrpc.method("RemoveContact(sessionCookie=str, otherUser=str) -> dict")
def RemoveContact(sessionCookie=str, otherUser=""):
    raise Exception("Not implemented yet")

@jsonrpc.method("BlockContact(sessionCookie=str, otherUser=str, silent=bool) -> dict")
def BlockContact(sessionCookie="", otherUser="", silent=False):
    raise Exception("Not implemented yet")

@jsonrpc.method("CreateUser(username=str, password=str, encryptedUserKeyPair=str, publicKey=str, privateKey=str) -> dict") 
def CreateUser(username="", password="", encryptedUserKeyPair="", publicKey="", privateKey=""):
    return xmpp2.CreateUser(username, password, encryptedUserKeyPair, publicKey, privateKey)
if __name__ == '__main__':
    app.run()
