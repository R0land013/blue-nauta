from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi


class MainView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__setup_gui()


    def __setup_gui(self):
        loadUi('./view/ui/main.ui', self)
        self.__setup_gui_connections()
    
    def __setup_gui_connections(self):
        self.init_session_button.clicked.connect(self.__presenter.open_session)
    
    def get_username(self) -> str:
        return self.user_line_edit.text().strip()
    
    def get_password(self) -> str:
        return self.password_line_edit.text().strip()