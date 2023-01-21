from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent
from view.main import MainView
from presenter.opened_session import OpenedSessionPresenter
from nautapy.nauta_api import NautaClient
from presenter.account_list import AccountListPresenter
from model.credentials.manager import CredentialManager
from model.entity.entity import UserCredential
from model.util.thread_worker import PresenterThreadWorker


class MainPresenter(AbstractPresenter):

    def _on_initialize(self):
        self.__initialize_view()
        self.__credential_manager = CredentialManager()
        self.__default_account: UserCredential = None
        self.__username: str = None
        self.__password: str = None
        self.__nauta_client: NautaClient = None

    def __initialize_view(self):
        self._set_view(MainView(self))

    def get_default_window_title(self) -> str:
        return 'Blue Nauta'

    def try_to_open_session(self):
        self.__username = self.get_view().get_username()
        self.__password = self.get_view().get_password()

        self.__open_session_thread = PresenterThreadWorker(
            self.__open_session_in_another_thread)

        self.__open_session_thread.when_started.connect(
            lambda: self.get_view().disable_all_gui(True))
        self.__open_session_thread.when_started.connect(
            lambda: self.get_view().set_status_text('Conectando...'))
        
        
        self.__open_session_thread.when_finished.connect(
            lambda: self.get_view().disable_all_gui(False)
        )
        self.__open_session_thread.when_finished.connect(
            lambda: self.get_view().set_status_text(''))

        self.__open_session_thread.finished_without_error.connect(
            self.__show_opened_session_presenter)
        
        self.__open_session_thread.start()
        

    def __open_session_in_another_thread(self, thread: PresenterThreadWorker):
        self.__nauta_client = NautaClient(
            user=self.__username, password=self.__password)
        self.__nauta_client.login()

        thread.finished_without_error.emit()

    def open_account_list_presenter(self):
        intent = Intent(AccountListPresenter)
        self._open_other_presenter(intent)

    def __show_opened_session_presenter(self):
        intent = Intent(OpenedSessionPresenter)
        data = {OpenedSessionPresenter.NAUTA_CLIENT_DATA: self.__nauta_client}
        intent.set_data(data)

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
