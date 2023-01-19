from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent
from view.main import MainView
from presenter.opened_session import OpenedSessionPresenter
from nautapy.nauta_api import NautaClient
from presenter.account_list import AccountListPresenter
from model.credentials.manager import CredentialManager
from model.entity.entity import UserCredential


class MainPresenter(AbstractPresenter):

    def _on_initialize(self):
        self.__initialize_view()
        self.__credential_manager = CredentialManager()
        self.__default_account: UserCredential = None

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

    def open_account_list_presenter(self):
        intent = Intent(AccountListPresenter)
        self._open_other_presenter(intent)

    def on_view_shown(self):
        self.load_default_account()

    def load_default_account(self):
        self.__default_account = self.__credential_manager.get_default_credential()
        view = self.get_view()
        if self.__default_account:
            view.set_username(self.__default_account.username)
            view.set_password(self.__default_account.password)
        else:
            view.set_username('')
            view.set_password('')

    def on_view_discovered_with_result(self, action: str, result_data: dict, result: str):
        
        if result == AccountListPresenter.USER_CHANGED_DEFAULT_ACCOUNT:
            self.load_default_account()