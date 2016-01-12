class CatMailContact:
    def has_avatar(self):
        #TODO not yet implemented
        return False

    def getContactID(self):
        return self.cid

    def getAlias(self):
        return self.alias if not self.alias is None and self.alias != "" else self.cid

    def equals(self, contact):
        return (
                self.getContactID() == contact.getContactID()
                and self.getAlias() == contact.getAlias()
            )

    def __init__(self, cid, alias=None):
        print(cid)
        self.cid = cid
        self.alias = alias
