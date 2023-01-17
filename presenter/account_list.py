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
        
    
    def __load_account_list(self):
        self.__credentials = CredentialManager().get_credentials()
        
        view = self.get_view()
        view.clear_account_list()
        for a_credential in self.__credentials:
            on_edit = lambda: print(a_credential.username)
            view.add_account(a_credential.username, on_edit)

    def on_view_discovered_with_result(self, action: str, result_data: dict, result: str):
        print(result, AccountFormPresenter.NEW_ACCOUNT_RESULT, result == AccountFormPresenter.NEW_ACCOUNT_RESULT)
        if result == AccountFormPresenter.NEW_ACCOUNT_RESULT:
            self.__load_account_list()