from PyQt5.QtWidgets import QWidget, QListWidget, QTextEdit, QVBoxLayout, \
        QHBoxLayout, QGridLayout, QTabWidget, QListWidgetItem, QLabel
from PyQt5.QtCore import pyqtSlot, pyqtSignal, Qt, QEvent, QObject
from .helpers import create_avatar

class Message(QWidget):
    def __init_ui(self):
        layout = QGridLayout(self)
        #TODO if self.avatar is None
        #TODO should we make this dynamic/configurable/...?
        self.avatar.setFixedSize(35, 35)
        layout.addWidget(self.avatar, 0, 0, 2, 1, alignment=Qt.AlignTop)

        text = QLabel(self)
        text.setText(self.message)
        text.setWordWrap(True)
        text.setTextInteractionFlags(Qt.TextSelectableByMouse)

        time = QLabel(self)
        time.setText(self.time)
        time.setStyleSheet('color: gray; font-size: 10px;')

        layout.addWidget(text, 0, 1, 1, 2)
        layout.addWidget(time, 1, 2)

        self.setLayout(layout)

    def __init__(self, avatar, time, message, its_me):
        super(Message, self).__init__()
        self.avatar = avatar
        self.time = time
        self.message = message
        self.its_me = its_me

        self.__init_ui()

class MessageListWidget(QListWidget):
    def add_message(self, sender, time, message, its_me):
        item = QListWidgetItem(self)
        #TODO move avatar creation out of here and buffer avatars
        avatar = create_avatar(sender)
        message = Message(avatar, time, message, its_me)
        item.setSizeHint(message.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, message)

    def __init__(self):
        super(MessageListWidget, self).__init__()

class MessageSendTextEditWidget(QTextEdit):
    send_message = pyqtSignal(str, name='sendMessage')

    def __send_message(self):
        message = self.toPlainText() # TODO read message
        self.clear()
        self.send_message.emit(message)

    def eventFilter(self, obj, ev):
        if (obj == self and ev.type() == QEvent.KeyPress):
            if (ev.key() == Qt.Key_Return
                    and ev.modifiers() != Qt.ShiftModifier):
                self.__send_message()
                return True # filter event, no further processing
        return False

    def __init__(self):
        super(MessageSendTextEditWidget, self).__init__()
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        self.installEventFilter(self)

class ConversationWidget(QWidget):
    send_message = pyqtSignal(str, str, name='sendMessage')

    def add_message(self, sender, time, message, its_me=False):
        self.messageList.add_message(sender, time, message, its_me)

    def __init_ui(self):
        layout = QVBoxLayout(self)

        self.messageList = MessageListWidget()
        layout.addWidget(self.messageList)

        layout.addSpacing(10)

        self.__sendEdit = MessageSendTextEditWidget()
        layout.addWidget(self.__sendEdit)

        self.setLayout(layout)

    def __send_message(self, message):
        self.send_message.emit(message, self.__conversationID)

    def __connect_signals(self):
        self.__sendEdit.send_message.connect(self.__send_message)

    def __init__(self, conversationID):
        super(ConversationWidget, self).__init__()
        self.known_contacts = []
        self.messageList = None
        self.__conversationID = conversationID
        self.__init_ui()
        self.__connect_signals()

class ConversationsViewManager(QObject):
    send_message = pyqtSignal(str, str, name='sendMessage')

    def __getConversationsWidgetById(self, conversationId):
        conversationsWidget = None
        if not conversationId is None:
            for cid, widget in self.conversations:
                if (cid == conversationId):
                    conversationsWidget = widget
                    break;
        return conversationsWidget

    def __setTab(self, conversationId, title, widget=None):
        conversationsWidget = widget if not widget is None \
                else self.__getConversationsWidgetById(conversationId)
        if not conversationsWidget is None:
            self.tab_widget.addTab(
                    conversationsWidget,
                    title if not title is None else conversationId
                )

    def get_widget(self):
        return self.tab_widget

    def set_conversationsTitle(self, conversationId, title):
        # Using the addTab method in __setTab allows us to change the title
        # without searching for the tab ID
        self.__setTab(conversationId, title)

    def add_conversation(self, conversationId, title=None):
        conversationsWidget = ConversationWidget(conversationId)
        self.conversations.append((conversationId, conversationsWidget))
        conversationsWidget.send_message.connect(self.__send_message)
        self.__setTab(conversationId, title, conversationsWidget)

    def add_message(self, conversationId, sender, time, message, its_me=False):
        widget = self.__getConversationsWidgetById(conversationId)
        if widget is None:
            #TODO should we implicitly call add_conversation
            raise RuntimeError('Conversation must be added before.')
        widget.add_message(sender, time, message, its_me)

    @pyqtSlot(int)
    def __on_tab_closed(self, index):
        print("Removing index %d" % index)
        self.tab_widget.removeTab(index)
        todel = self.conversationsWidget.pop(index)
        #TODO emit chat closed
        del(todel[1]) # only remove the widget, not the id #TODO

    def __init_ui(self):
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.setMovable(True)
        self.tab_widget.tabCloseRequested.connect(self.__on_tab_closed)

    def __send_message(self, message, conversationID):
        self.send_message.emit(message, conversationID)

    def __init__(self, parent=None):
        super(ConversationsViewManager, self).__init__()
        self.tab_widget = QTabWidget(parent)
        self.__init_ui()
        self.conversations = []
