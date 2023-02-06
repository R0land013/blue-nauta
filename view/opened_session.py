from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer
from datetime import timedelta
from PyQt5.QtWidgets import QMessageBox


class OpenedSessionView(QFrame):

    def __init__(self, presenter):
        super().__init__()

        self.__presenter = presenter
        self.__time_counter = QTimer(self)
        self.__consumed_seconds = 0
        self.__time_counter.timeout.connect(self.set_consumed_time)
        self.__setup_gui()
    
    def __setup_gui(self):
        loadUi('./view/ui/opened_session.ui', self)
        self.__setup_gui_connections()
    
    def __setup_gui_connections(self):
        self.close_session_button.clicked.connect(self.__presenter.close_session)
    
    def set_available_time(self, available_time: str):
        self.available_time_label.setText(available_time)
    
    def set_consumed_time(self):
        self.__consumed_seconds += 1
        self.consumed_time_label.setText(str(timedelta(seconds=self.__consumed_seconds)))

    def start_time_counter(self):
        self.__time_counter.start(1000)
    
    def stop_time_counter(self):
        self.__time_counter.stop()
    
    def disable_gui(self, disabled: bool):
        self.close_session_button.setDisabled(disabled)
    
    def show_dialog_error_message(self, message: str):
        QMessageBox.critical(self.window(), 'Error', message)