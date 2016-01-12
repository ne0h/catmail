class ClientBackend:
    def update_contacts(self):
        raise NotImplementedError()

    def __init__(self):
        pass

class ClientInterface:
    def first_run(self):
        raise NotImplementedError()

    def show(self):
        raise NotImplementedError()

    def __init__(self):
        pass
