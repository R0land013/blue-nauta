from PyQt5.QtWidgets import QFrame, QMessageBox
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
        self.init_session_button.clicked.connect(self.__presenter.try_to_open_session)
        self.show_accounts_button.clicked.connect(self.__presenter.open_account_list_presenter)
    
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
    
    def set_status_text(self, status: str):
        self.status_label.setText(status)

    def show_dialog_error_message(self, message: str):
        QMessageBox.critical(self.window(), 'Error', message)