from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel
from random import randint

def __random_color():
    colors = ['red', 'green', 'blue', 'orange', 'fuchsia', 'lime']
    return colors[randint(0, len(colors) - 1)]

def create_avatar(contact, existing_avatar=None, parent=None):
    avatar = QLabel(parent) if existing_avatar is None else existing_avatar
    if contact.has_avatar():
    #    pic = QPixmap()
    #    pic.load()
    #    avatar.setPixmap(pic)
        pass
    else:
        avatar.setStyleSheet(
                "background-color: %s; " \
                "font-weight: bold; " \
                "font-size: 20px;" % __random_color()
            );
        text = contact.getAlias()
        avatar.setText(text[0] if text != "" else contact.getContactID()[0])
    avatar.setAlignment(Qt.AlignCenter)
    avatar.setFixedSize(20, 20)
    return avatar
