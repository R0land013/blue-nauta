from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent
from view.main import MainView
from presenter.opened_session import OpenedSessionPresenter
from nautapy.nauta_api import NautaClient


class MainPresenter(AbstractPresenter):

    def _on_initialize(self):
        self.__initialize_view()

    def __initialize_view(self):
        self._set_view(MainView(self))

    def get_default_window_title(self) -> str:
        return 'Blue Nauta'
    
    def open_session(self):
        username = self.get_view().get_username()
        password = self.get_view().get_password()

        nauta_client = NautaClient(user=username, password=password)
        nauta_client.login()

        intent = Intent(OpenedSessionPresenter)
        data = {OpenedSessionPresenter.NAUTA_CLIENT_DATA: nauta_client}
        intent.set_data(data)
        
        self._open_other_presenter(intent)
