from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi


class OpenedSessionView(QFrame):

    def __init__(self, presenter):
        super().__init__()

        self.__presenter = presenter
        self.__setup_gui()
    
    def __setup_gui(self):
        loadUi('./view/ui/opened_session.ui', self)
        self.__setup_gui_connections()
    
    def __setup_gui_connections(self):
        self.close_session_button.clicked.connect(self.__presenter.close_session)
    
    def set_available_time(self, available_time: str):
        self.available_time_label.setText(available_time)