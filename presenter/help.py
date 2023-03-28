from easy_mvp.abstract_presenter import AbstractPresenter
from view.help import HelpView


class HelpPresenter(AbstractPresenter):

    def _on_initialize(self):
        self._set_view(HelpView(self))
    
    def go_back(self):
        self._close_this_presenter()

    def get_default_window_title(self) -> str:
        return 'Blue Nauta - Ayuda'
