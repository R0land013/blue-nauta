from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent
from view.account_list import AccountListView
from presenter.account_form import AccountFormPresenter
from model.credentials.manager import CredentialManager
from model.entity.entity import UserCredential
from typing import List


class AccountListPresenter(AbstractPresenter):

    USER_CHANGED_DEFAULT_ACCOUNT = 'user_changed_default_account'

    def _on_initialize(self):
        self.__initialize_view()
        self.__credentials: List[UserCredential] = None
        self.__credential_manager: CredentialManager = CredentialManager()
        self.__user_has_changed_default_account = False

    def __initialize_view(self):
        self._set_view(AccountListView(self))

    def return_to_main_view(self):
        if self.__user_has_changed_default_account:
            self.__notify_main_presenter_user_has_changed_default_account()
        else:
            self._close_this_presenter()

    def __notify_main_presenter_user_has_changed_default_account(self):
        self._close_this_presenter_with_result(
            result_data={}, result=self.USER_CHANGED_DEFAULT_ACCOUNT)

    def get_default_window_title(self) -> str:
        return 'Blue Nauta - Lista de cuentas'

    def open_account_form_presenter_for_adding_account(self):
        intent = Intent(AccountFormPresenter)
        intent.set_action(AccountFormPresenter.NEW_ACCOUNT_ACTION)
        intent.use_new_window(True)
        intent.use_modal(True)

        self._open_other_presenter(intent)

    def on_view_shown(self):
        self.__load_account_list()
        self.__set_accounts_for_selecting_default()
        self.__set_selected_default_account()

    def __load_account_list(self):
        self.__credentials = CredentialManager().get_credentials()
        self.__credentials = sorted(
            self.__credentials, key=lambda account: account.username)

        self.get_view().clear_account_list()
        for a_credential in self.__credentials:
            self.__add_an_account(a_credential)

    def __add_an_account(self, account: UserCredential):
        def on_edit(): return self.__open_account_form_presenter_for_editing(account)
        self.get_view().add_account(account.username, on_edit)

    def __open_account_form_presenter_for_editing(self, account: UserCredential):
        intent = Intent(AccountFormPresenter)
        intent.set_action(AccountFormPresenter.EDIT_ACCOUNT_ACTION)
        data = {AccountFormPresenter.ACCOUNT_TO_EDIT_DATA: account}
        intent.set_data(data)

        intent.use_new_window(True)
        intent.use_modal(True)

        self._open_other_presenter(intent)

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

        if (result == AccountFormPresenter.NEW_ACCOUNT_RESULT or
                result == AccountFormPresenter.EDITED_ACCOUNT_RESULT):

            self.on_view_shown()

    def handle_use_default_account(self, use_default_account: bool, account_id: int = -1):
        self.__user_has_changed_default_account = True

        if use_default_account and account_id != -1:
            self.handle_default_account_changed(account_id)
        else:
            self.__credential_manager.clear_default_credentials()

    def handle_default_account_changed(self, account_id: int):
        self.__user_has_changed_default_account = True
        default_account: UserCredential = None

        for account in self.__credentials:
            if account.id == account_id:
                default_account = account
        if default_account:
            self.__credential_manager.set_account_as_default(default_account)
