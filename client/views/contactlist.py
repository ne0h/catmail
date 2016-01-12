from PyQt5.QtWidgets import QWidget, QGridLayout, QListWidget, \
        QListWidgetItem, QLabel, QTabWidget
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QObject, Qt
from contact import CatMailContact
from random import randint
from .helpers import create_avatar

class ContactListEntry(QWidget):
    def __click_cb(self):
        if not self.callback is None:
            self.callback(self.contact_id)

    def get_widget(self):
        return self

    def update(self, contact):
        self.name.setText(contact.getAlias())
        self.contact_id = contact.getContactID()
        self.avatar = create_avatar(contact, self.avatar)

    def __init_ui(self, contact):
        height = 20
        grid = QGridLayout(self)
        grid.setSpacing(0)
        grid.setContentsMargins(0,0,0,0)
        grid.setSizeConstraint(QGridLayout.SetFixedSize)

        self.setLayout(grid)

        self.avatar.resize(height, height)
        grid.addWidget(self.avatar, 0, 0)

        self.name = QLabel(self)
        self.name.resize(self.name.sizeHint())
        #addWidget(widget, y, x, yspan, xspan)
        grid.addWidget(self.name, 0, 1)

        self.setMinimumHeight(height)
        #self.widget.clicked.connect(self.__click_cb)

        self.update(contact)

    def get_cid(self):
        return self.cid

    def __init__(self, parent, contact, callback=None):
        super(ContactListEntry, self).__init__(parent)
        print('init contact')
        self.callback = callback
        self.avatar = QLabel()
        self.cid = contact.getContactID()
        #self.widget = QWidget()
        self.__init_ui(contact)

class ContactListManager(QObject):
    contact_db_clicked = pyqtSignal(str, name="contact_db_clicked")

    def __get_contact_id_by_widget_id(self, list_item):
        contactWidget = self.__contactlist.item(list_item)
        return contactWidget.get_cid() if not contactWidget is None else None

    @pyqtSlot(QListWidgetItem)
    def __on_contact_db_clicked(self, list_widget_item):
        print("__on_contact_db_clicked")
        if not list_widget_item is None \
                and not list_widget_item.data(Qt.UserRole) is None \
            :
                self.contact_db_clicked.emit(
                        list_widget_item.data(Qt.UserRole).get_cid()
                    )

    @pyqtSlot(QListWidgetItem)
    def __on_conversation_db_clicked(list_item):
        print("__on_conversation_db_clicked")

    def __add_contact(self, contact):
        item = QListWidgetItem(self.__contactlist)
        c = ContactListEntry(self.__contactlist, contact)
        item.setSizeHint(c.sizeHint())
        item.setData(Qt.UserRole, c)
        self.__contactlist.addItem(item)
        self.__contactlist.setItemWidget(item, c)

    def __add_conversation(self, conversation):
        pass

    def get_widget(self):
        return self.tab_widget

    def update_contacts(self):
        if not self.__catmail_contact_list is None:
            for c in self.__catmail_contact_list.get_contacts_iterator():
                print("contact test: %s" % str(c))
                self.__add_contact(c)
        #cts = contacts if isinstance(contacts, list) else [contacts]

        #for c in cts:
        #    self.__add_contact(c)

    def set_contact_list(self, contact_list):
        self.__catmail_contact_list = contact_list

    def __init_ui(self):
        self.tab_widget.setTabsClosable(False)
        self.tab_widget.setMovable(False)

    #TODO swap tabs
        self.tab_widget.addTab(self.__contactlist, "Contacts")
        self.tab_widget.addTab(self.__conversationlist, "Conversations")
    #TODO if there are no conversations, switch to contacts.

    def __connect_signals(self):
        self.__contactlist.itemDoubleClicked.connect(
     #           self.contact_db_clicked
                self.__on_contact_db_clicked
            )
        self.__conversationlist.itemDoubleClicked.connect(
                self.__on_conversation_db_clicked
            )

    def __init__(self, parent=None):
        super(ContactListManager, self).__init__()
        self.tab_widget = QTabWidget(parent)

        self.__contactlist = QListWidget(self.tab_widget)
        self.__conversationlist = QListWidget(self.tab_widget)
        self.__catmail_contact_list = None

        self.__init_ui()
        self.__connect_signals()
