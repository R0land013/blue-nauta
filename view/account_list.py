from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi


class AccountListView(QFrame):

    def __init__(self, presenter) -> None:
        super().__init__()
        self.__presenter = presenter

        self.__setup_gui()

    def __setup_gui(self):
        loadUi('./view/ui/account_list.ui', self)
        self.__setup_gui_connections()

    def __setup_gui_connections(self):
        self.go_back_button.clicked.connect(
            self.__presenter.return_to_main_view)
        self.new_account_button.clicked.connect(
            self.__presenter.open_account_form_presenter)
