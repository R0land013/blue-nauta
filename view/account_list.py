from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.uic import loadUi
from typing import Callable


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

    def clear_account_list(self):
        # Linking the old account list layout to other widget and
        # unlinking it from account list frame
        auxiliary_widget = QWidget()
        auxiliary_widget.setLayout(self.account_list_frame.layout())
        auxiliary_widget.deleteLater()

        self.account_list_frame.setLayout(QVBoxLayout(self.account_list_frame))

    def add_account(self, username: str, on_edit_pressed: Callable):
        account_frame = QFrame(parent=self.account_list_frame)
        
        layout = QHBoxLayout(account_frame)
        layout.addWidget(QLabel(username))
        edit_button = QPushButton('Editar')
        edit_button.clicked.connect(on_edit_pressed)
        layout.addWidget(edit_button)
        account_frame.setLayout(layout)

        list_frame_layout = self.account_list_frame.layout()
        list_frame_layout.addWidget(account_frame)
        account_frame.show()
