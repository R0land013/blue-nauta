from easy_mvp.abstract_presenter import AbstractPresenter
from view.main import MainView


class MainPresenter(AbstractPresenter):

    def _on_initialize(self):
        self.__initialize_view()

    def __initialize_view(self):
        self._set_view(MainView(self))

    def get_default_window_title(self) -> str:
        return 'Blue Nauta'