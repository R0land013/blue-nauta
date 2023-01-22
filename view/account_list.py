from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from typing import Callable
from typing import List, Tuple


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
            self.__presenter.open_account_form_presenter_for_adding_account)

        self.use_default_account_check_box.stateChanged.connect(
            self.__notify_presenter_on_use_default_account_changed)

        self.default_account_combo_box.currentIndexChanged.connect(
            self.__notify_presenter_on_default_account_changed
        )

    def __notify_presenter_on_use_default_account_changed(self, check_state):
        if check_state == Qt.Unchecked:
            self.default_account_combo_box.setEnabled(False)
            self.__presenter.handle_use_default_account(False, account_id=-1)
        else:
            self.default_account_combo_box.setEnabled(True)
            account_quantity = self.default_account_combo_box.count()
            account_id = -1
            if account_quantity > 0:
                account_id = self.default_account_combo_box.currentData()
            self.__presenter.handle_use_default_account(True, account_id)

    def __notify_presenter_on_default_account_changed(self):

        if self.use_default_account_check_box.checkState() == Qt.Checked:
            account_id = self.default_account_combo_box.currentData()
            self.__presenter.handle_default_account_changed(account_id)

    def set_accounts_for_selecting_default(self, accounts: List[Tuple[str, int]]):
        self.default_account_combo_box.clear()
        for an_account in accounts:
            self.default_account_combo_box.addItem(
                an_account[0], an_account[1])
        
        if len(accounts) > 0:
            self.use_default_account_check_box.setEnabled(True)
        else:
            self.use_default_account_check_box.setEnabled(False)

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

    def set_selected_account(self, account_id: int):
        account_quantity = self.default_account_combo_box.count()
        for account_index in range(account_quantity):
            an_account_id = self.default_account_combo_box.itemData(
                account_index)
            if an_account_id == account_id:
                self.use_default_account_check_box.setCheckState(Qt.Checked)
                self.default_account_combo_box.setCurrentIndex(account_index)

