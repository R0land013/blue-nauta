from PyQt5.QtWidgets import QFrame
from PyQt5.uic import loadUi


class MainView(QFrame):

    def __init__(self, presenter):
        super().__init__()
        self.__presenter = presenter

        self.__setup_gui()


    def __setup_gui(self):
        loadUi('./view/ui/main.ui', self)