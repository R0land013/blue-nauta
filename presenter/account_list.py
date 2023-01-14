from easy_mvp.abstract_presenter import AbstractPresenter
from easy_mvp.intent import Intent
from view.account_list import AccountListView
from presenter.account_form import AccountFormPresenter


class AccountListPresenter(AbstractPresenter):

    def _on_initialize(self):
        self.__initialize_view()
    
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
