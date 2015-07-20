import time
import sqlite3
from helpfunctions import getRandomChallenge

__author__ = 'adrian'
class XMPP2:
    randomChallenges = {}
    def __init__(self):
        sqlite_connection = sqlite3.connect('database.sqlite')
        sqlite_connection.cursor()


        #Check if Databse is alread initiliase else initilise Database
        if sqlite_connection.execute("SELECT count(*) FROM sqlite_master WHERE type = 'table' AND name = 'user_table';").fetchone()[0] == 1:
            pass
        else :
            sqlite_connection.execute("CREATE TABLE user_table(USERNAME CHAR(50) PRIMARY KEY NOT NULL, PASSWORD CHAR(50) NOT NULL, ENCRYPTED_KEYPAIR CHAR(50) NOT NULL, PRIVAT_KEY CHAR(50) NOT NULL, PUBLIC_KEY CHAR(50) NOT NULL);")
           
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
        if sqlite_connection.execute("SELECT count(*) FROM user_table WHERE USERNAME = " + user_table + ";").fetchone()[0] == 0:
            sqlite_connection.execute("INSERT INTO user_table (USERNAME, PASSWORD, ENCRYPTED_KEYPAIR, PUBLIC_KEY, PRIVAT_KEY) VALUES (" + username +"," + password + "," + encryptedKeypair + "," + publicKey + "," + privatKey +");")
            sqlite_connection.commit()
            return()
        else:
            raise Exception("Username already taken")

    def __exit__(self, type, value, traceback):
        sqlite_connection.close()