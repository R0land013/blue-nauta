from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi
from util.resources_path import resource_path


class HelpView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__setup_gui()
    
    def __setup_gui(self):
        loadUi(resource_path('view/ui/help.ui'), self)
        self.__setup_gui_connections()

    def __setup_gui_connections(self):
        self.back_button.clicked.connect(self.__presenter.go_back)