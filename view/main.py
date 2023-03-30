from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QFrame, QMessageBox, QLineEdit
from PyQt5.uic import loadUi
from util.resources_path import resource_path


class MainView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__setup_gui()

    def __setup_gui(self):
        loadUi(resource_path('view/ui/main.ui'), self)
        # set windows icon (it doesn't work)
        self.setWindowIcon(QIcon(resource_path('view/ui/assets/bluenauta.png')))
        # toggle password visibility button on line edit
        self.visibleIcon = QIcon(resource_path('view/ui/assets/show.png'))
        self.hiddenIcon = QIcon(resource_path('view/ui/assets/hide.png'))
        self.togglepasswordAction = self.password_line_edit.addAction(self.visibleIcon,
                                                                      QLineEdit.ActionPosition.TrailingPosition)
        self.togglepasswordAction.triggered.connect(
            self.__on_toggle_password_action)

        self.__setup_gui_connections()

    def __on_toggle_password_action(self):
        if self.password_line_edit.echoMode() == QLineEdit.Password:
            self.password_line_edit.setEchoMode(QLineEdit.Normal)
            self.togglepasswordAction.setIcon(self.hiddenIcon)
        else:
            self.password_line_edit.setEchoMode(QLineEdit.Password)
            self.togglepasswordAction.setIcon(self.visibleIcon)

    def __setup_gui_connections(self):
        self.init_session_button.clicked.connect(
            self.__presenter.try_to_open_session)
        self.show_accounts_button.clicked.connect(
            self.__presenter.open_account_list_presenter)
        self.help_button.clicked.connect(self.__presenter.open_help_presenter)

    def get_username(self) -> str:
        return self.user_line_edit.text().strip()

    def set_username(self, username: str):
        self.user_line_edit.setText(username)

    def get_password(self) -> str:
        return self.password_line_edit.text().strip()

    def set_password(self, password: str):
        self.password_line_edit.setText(password)

    def disable_all_gui(self, disabled: bool):
        self.main_container.setDisabled(disabled)
        self.superior_bar.setDisabled(disabled)

    def set_status_text(self, status: str):
        self.status_label.setText(status)

    def show_dialog_error_message(self, message: str):
        QMessageBox.critical(self.window(), 'Error', message)
