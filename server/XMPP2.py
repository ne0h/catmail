import time
import sqlite3
from helpfunctions import getRandomChallenge
__author__ = 'adrian'
class XMPP2:
    randomChallenges = {}
    def __init__(self):
        pass

    def openDatabaseConnection(self):
        self.sqlite_connection = sqlite3.connect('database.sqlite')
        self.sqlite_connection.cursor()


        #Check if Databse is alread initiliase else initilise Database
        if self.sqlite_connection.execute("SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name = 'user_table';").fetchone()[0] == 1:
            pass
        else :
            self.sqlite_connection.execute("CREATE TABLE user_table(USERNAME TEXT PRIMARY KEY NOT NULL,PASSWORD TEXT NOT NULL, USERKEY_SECRETKEY TEXT NOT NULL, USERKEY_NONCE TEXT NOT NULL, USERKEY_PUBLICKEY TEXT NOT NULL, EXCHANGEKEY_SECRETKEY TEXT NOT NULL, EXCHANGEKEY_NONCE TEXT NOT NULL, EXCHANGEKEY_PUBLICKEY TEXT NOT NULL);")
       
    def closeDatabaseConnection(self):
        self.sqlite_connection.close()
    def requestLoginChallenge(self, user, protocolVersion):
        randomChallenge = getRandomChallenge()
        self.randomChallenges[randomChallenge] = [time.time() + 60, user]
        return {"challenge": randomChallenge}

    def login(self, user, clientID, loginChallenge, loginSignature):
        challenges = [self.randomChallenges[n] for n in self.randomChallenges if n == loginChallenge]
        raise Exception("Not implemented yet")
        

    def logout(self, sessionCookie):
        raise Exception("Not implemented yet")
        pass

    def getUserPublicKeys(self, sessionCookie, otherUser):
        raise Exception("Not implemented yet")
        pass

    def pollChatMessages(self, sessionCookie):
        raise Exception("Not implemented yet")
        pass

    def createUser(self, username, password, userKey, exchangeKey):
        print(userKey["secretKey"])
        self.openDatabaseConnection()
        print("SELECT count(*) FROM user_table WHERE USERNAME = '" + username + "';")
        if self.sqlite_connection.execute("SELECT count(*) FROM user_table where USERNAME = '" + username + "';").fetchone()[0] == 0: #check if the username already exists
            self.sqlite_connection.execute("INSERT INTO user_table (USERNAME, PASSWORD, USERKEY_SECRETKEY, 
USERKEY_NONCE, USERKEY_PUBLICKYE, EXCHANGEKEY_SECRETKEY, EXCHANGEKEY_NONCE, EXCHANGEKEY_PUBLICKEY) VALUES ('" + username +"','" + password + "','" + userKey["secretKey"] + "','" + userKey["nonce"] + "','" + userKey["publicKey"] + "','" + exchangeKey["secretKey"] + "','" + exchangeKey["nonce"] + "','" + exchangeKey["publicKey"] +  "');")
            self.sqlite_connection.commit()
            self.closeDatabaseConnection()
            return {"result": 0}
        else:
            return {"result": -1}
            

    def __exit__(self, type, value, traceback):
        return
