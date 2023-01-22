from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi


class AccountFormView(QFrame):

    def __init__(self, presenter):
        super().__init__()

        self.__presenter = presenter
        self.__setup_gui()
    
    def __setup_gui(self):
        loadUi('./view/ui/account_form.ui', self)
        self.__setup_gui_connections()
    
    def __setup_gui_connections(self):
        self.cancel_button.clicked.connect(self.__presenter.close_form)
        self.save_button.clicked.connect(self.__presenter.save_account_and_close_presenter)
    
    def get_username(self):
        return self.username_line_edit.text().strip()
    
    def set_username(self, username: str):
        self.username_line_edit.setText(username)

    def get_password(self):
        return self.password_line_edit.text().strip()
    
    def set_password(self, password: str):
        self.password_line_edit.setText(password)
