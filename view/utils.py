from PyQt5.QtWidgets import QMessageBox


def show_action_confirmation_dialog(view, title:str, message: str):
    q = QMessageBox.question(view, title, message,
                             QMessageBox.Yes | QMessageBox.No)
    if q == QMessageBox.Yes:
        return True
    return False