from PyQt5.QtWidgets import QMessageBox, QPushButton
from PyQt5.QtCore import Qt


def show_action_confirmation_dialog(view, title:str, message: str):
    message_box = QMessageBox(view)
    message_box.setIcon(QMessageBox.Question)
    message_box.setWindowTitle(title)
    message_box.setText(message)
    message_box.setStyleSheet('QLabel { color : black; }')

    yes_button = QPushButton('Sí')
    yes_button.setCursor(Qt.PointingHandCursor)
    no_button = QPushButton('No')
    no_button.setCursor(Qt.PointingHandCursor)

    message_box.addButton(yes_button, QMessageBox.AcceptRole)
    message_box.addButton(no_button, QMessageBox.NoRole)

    message_box.exec()
    return message_box.clickedButton() == yes_button
