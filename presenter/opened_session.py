from easy_mvp.abstract_presenter import AbstractPresenter
from view.opened_session import OpenedSessionView
from nautapy.nauta_api import NautaClient


class OpenedSessionPresenter(AbstractPresenter):

    NAUTA_CLIENT_DATA = 'nauta_client_data'

    def _on_initialize(self):
        self.__initialize_view()
        self.__nauta_client: NautaClient = self._get_intent_data()[self.NAUTA_CLIENT_DATA]

    def __initialize_view(self):
        self._set_view(OpenedSessionView(self))
    
    def on_view_shown(self):
        self.get_view().set_available_time(self.__nauta_client.remaining_time)
    
    def get_default_window_title(self) -> str:
        return 'Sesión iniciada'
    
    def close_session(self):
        self.__nauta_client.logout()
        self._close_this_presenter()