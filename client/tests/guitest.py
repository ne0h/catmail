import datetime
import sys
sys.path.append('../')

from PyQt5.QtWidgets import QApplication
from catmailclient import CatMailClient
from contact import CatMailContact

def __get_dummy_contacts():
    contacts = []
    for i in range(0, 10):
        c = CatMailContact("Contact %s" % i)
        contacts.append(c)
        print(c.getAlias())
    return contacts


if __name__ == '__main__':
    app = QApplication([])
    gui = CatMailClient()
    gui.init(None)
    gui.show()

    conversations = ['foo@bar.com', 'cat@mail.de']
    contacts = __get_dummy_contacts()

    gui.update_contacts(contacts)
    gui.add_conversation(contacts[0].getContactID(), contacts[0].getAlias())
    gui.add_message(
            contacts[0].getContactID(),
            contacts[0],
            datetime.datetime.now().__str__(),
            'Lorem ipsum dolor sit amet, ...'
            )
    gui.add_message(
            contacts[0].getContactID(),
            contacts[0],
            datetime.datetime.now().__str__(),
            '... consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. '
            )
    gui.add_message(
            contacts[0].getContactID(),
            contacts[0],
            datetime.datetime.now().__str__(),
            'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.\nDuis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.\nExcepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.'
            )

    app.exec_()
