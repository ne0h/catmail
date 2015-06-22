import time
from helpfunctions import getRandomChallenge

__author__ = 'adrian'


class XMPP2:
    randomChallenges = {}
    def __init__(self):
        pass

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