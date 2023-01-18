from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent
from view.account_list import AccountListView
from presenter.account_form import AccountFormPresenter
from model.credentials.manager import CredentialManager
from model.entity.entity import UserCredential
from typing import List


class AccountListPresenter(AbstractPresenter):

    def _on_initialize(self):
        self.__initialize_view()
        self.__credentials: List[UserCredential] = None
        self.__credential_manager: CredentialManager = CredentialManager()

    def __initialize_view(self):
        self._set_view(AccountListView(self))

    def return_to_main_view(self):
        self._close_this_presenter()

    def get_default_window_title(self) -> str:
        return 'Blue Nauta - Lista de cuentas'

    def open_account_form_presenter(self):
        intent = Intent(AccountFormPresenter)
        intent.use_new_window(True)
        intent.use_modal(True)

        self._open_other_presenter(intent)

    def on_view_shown(self):
        self.__load_account_list()
        self.__set_accounts_for_selecting_default()
        self.__set_selected_default_account()

    def __load_account_list(self):
        self.__credentials = CredentialManager().get_credentials()
        self.__credentials = sorted(self.__credentials, key=lambda account: account.username)

        view = self.get_view()
        view.clear_account_list()
        for a_credential in self.__credentials:
            def on_edit(): return print(a_credential.username)
            view.add_account(a_credential.username, on_edit)

    def __set_accounts_for_selecting_default(self):
        usernames_and_ids = map(lambda account: (
            account.username, account.id), self.__credentials)
        self.get_view().set_accounts_for_selecting_default(list(usernames_and_ids))
    
    def __set_selected_default_account(self):
        selected_account: UserCredential = None
        for account in self.__credentials:
            if account.is_default:
                selected_account = account
        
        if selected_account:
            self.get_view().set_selected_account(selected_account.id)

    def on_view_discovered_with_result(self, action: str, result_data: dict, result: str):
        
        if result == AccountFormPresenter.NEW_ACCOUNT_RESULT:
            self.on_view_shown()

    def handle_use_default_account(self, use_default_account: bool, account_id: int = -1):
        if use_default_account and account_id != -1:
            self.handle_default_account_changed(account_id)
        else:
            self.__credential_manager.clear_default_credentials()

    def handle_default_account_changed(self, account_id: int):
        default_account: UserCredential = None

        for account in self.__credentials:
            if account.id == account_id:
                default_account = account
        if default_account:
            self.__credential_manager.set_account_as_default(default_account)
