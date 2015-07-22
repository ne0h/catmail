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
            self.sqlite_connection.execute("CREATE TABLE user_table(USERNAME TEXT PRIMARY KEY NOT NULL, PASSWORD TEXT NOT NULL, ENCRYPTED_KEYPAIR TEXT NOT NULL, PRIVAT_KEY TEXT NOT NULL, PUBLIC_KEY TEXT NOT NULL);")
       
    def closeDatabaseConnection(self):
        self.sqlite_connection.close()
    def RequestLoginChallenge(self, user, protocolVersion):
        randomChallenge = getRandomChallenge()
        self.randomChallenges[randomChallenge] = [time.time() + 60, user]
        return {"challenge": randomChallenge}

    def Login(self, user, clientID, loginChallenge, loginSignature):
        challenges = [self.randomChallenges[n] for n in self.randomChallenges if n == loginChallenge]
        raise Exception("Not implemented yet")
        

    def Logout(self, sessionCookie):
        raise Exception("Not implemented yet")
        pass

    def GetUserPublicKeys(self, sessionCookie, otherUser):
        raise Exception("Not implemented yet")
        pass

    def PollChatMessages(self, sessionCookie):
        raise Exception("Not implemented yet")
        pass
    def CreateUser(self, username, password, encryptedKeypair, publicKey, privatKey):
        self.openDatabaseConnection()
        print("SELECT count(*) FROM user_table WHERE USERNAME = '" + username + "';")
        if self.sqlite_connection.execute("SELECT count(*) FROM user_table where USERNAME = '" + username + "';").fetchone()[0] == 0:
            self.sqlite_connection.execute("INSERT INTO user_table (USERNAME, PASSWORD, ENCRYPTED_KEYPAIR, PUBLIC_KEY, PRIVAT_KEY) VALUES ('" + username +"','" + password + "','" + encryptedKeypair + "','" + publicKey + "','" + privatKey + "');")
            self.sqlite_connection.commit()
            self.closeDatabaseConnection()
            return {}
        else:
            raise Exception("Username already taken")

    def __exit__(self, type, value, traceback):
        return
