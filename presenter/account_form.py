from easy_mvp.abstract_presenter import AbstractPresenter
from view.account_form import AccountFormView
from model.credentials.manager import CredentialManager
from model.entity.entity import UserCredential


class AccountFormPresenter(AbstractPresenter):

    NEW_ACCOUNT_ACTION = 'new_account_action'
    EDIT_ACCOUNT_ACTION = 'edit_account_action'

    NEW_ACCOUNT_RESULT = 'new_account_result'
    EDITED_ACCOUNT_RESULT = 'edited_account_result'

    ACCOUNT_TO_EDIT_DATA = 'account_to_edit_data'

    def _on_initialize(self):
        self._set_view(AccountFormView(self))
        self.__account_to_edit: UserCredential = None
        
        if self._get_intent_action() == self.EDIT_ACCOUNT_ACTION:
            self.__account_to_edit = self._get_intent_data()[
                self.ACCOUNT_TO_EDIT_DATA]

    def close_form(self):
        self._close_this_presenter()

    def get_default_window_title(self) -> str:
        return 'Nueva cuenta'

    def on_view_shown(self):
        if self._get_intent_action() == self.EDIT_ACCOUNT_ACTION:
            self.__fill_form_fields()
    
    def __fill_form_fields(self):
        self.get_view().set_username(self.__account_to_edit.username)
        self.get_view().set_password(self.__account_to_edit.password)
    
    def save_account_and_close_presenter(self):

        if self._get_intent_action() == self.NEW_ACCOUNT_ACTION:
            self.save_new_account()

        elif self._get_intent_action() == self.EDIT_ACCOUNT_ACTION:
            self.update_account()

    def save_new_account(self):
        view = self.get_view()
        credential_manager = CredentialManager()
        credential_manager.save_username_and_password(
            username=view.get_username(),
            password=view.get_password())

        self._close_this_presenter_with_result(
            result_data=None,
            result=self.NEW_ACCOUNT_RESULT)

    def update_account(self):
        view = self.get_view()
        updated_credential = UserCredential(
            id=self.__account_to_edit.id,
            username=view.get_username(),
            password=view.get_password())
        
        credential_manager = CredentialManager()
        
        credential_manager.update_credential(updated_credential)

        self._close_this_presenter_with_result(
            result_data=None,
            result=self.EDITED_ACCOUNT_RESULT)