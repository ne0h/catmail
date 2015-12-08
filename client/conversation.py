class CatMailConversation:
    def has_avatar(self):
        #TODO not yet implemented
        return False

    def getConversationID(self):
        return self.cid

    def getAlias(self):
        return self.alias if not self.alias is None else self.cid

    def __check_participant(self, participant):
        if (not isinstance(participant, CatMailContact)):
            raise RuntimeError("Participant must be a CatMailContact.")

    def is_participant(self, participant):
        self.__check_participant(participant)
        rv = False
        for p in self.participants:
            if p.equals(participant):
                rv = True
                break;
        return rv

    def is_private(self):
        return (len(self.participants) == 1)

    def add_participant(self, participant):
        self.__check_participant(participant)
        self.append(participant)

    def __init__(self, cid, me, participants=[], alias=None):
        print(cid)
        self.cid = cid
        self.me = me
        self.participants = participants
        self.alias = alias
