from easy_mvp.abstract_presenter import AbstractPresenter
from view.account_form import AccountFormView
from model.credentials.manager import CredentialManager


class AccountFormPresenter(AbstractPresenter):

    NEW_ACCOUNT_RESULT = 'new_account_result'

    def _on_initialize(self):
        self._set_view(AccountFormView(self))

    def close_form(self):
        self._close_this_presenter()

    def get_default_window_title(self) -> str:
        return 'Nueva cuenta'

    def save_account_and_close_presenter(self):
        view = self.get_view()
        credential_manager = CredentialManager()
        credential_manager.save_username_and_password(
            username=view.get_username(),
            password=view.get_password())
        
        print(credential_manager.get_usernames())

        self._close_this_presenter_with_result(
            result_data=None,
            result=self.NEW_ACCOUNT_RESULT)




