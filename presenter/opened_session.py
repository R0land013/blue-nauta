from easy_mvp.abstract_presenter import AbstractPresenter
from view.opened_session import OpenedSessionView
from nautapy.nauta_api import NautaClient
from model.util.thread_worker import PresenterThreadWorker
from nautapy.exceptions import NautaLogoutException


class OpenedSessionPresenter(AbstractPresenter):

    NAUTA_CLIENT_DATA = 'nauta_client_data'

    def _on_initialize(self):
        self.__initialize_view()
        self.__nauta_client: NautaClient = self._get_intent_data()[
            self.NAUTA_CLIENT_DATA]

    def __initialize_view(self):
        self._set_view(OpenedSessionView(self))

    def on_view_shown(self):
        self.get_view().set_available_time(self.__nauta_client.remaining_time)
        self.get_view().start_time_counter()

    def get_default_window_title(self) -> str:
        return 'Sesión iniciada'

    def close_session(self):
        self.thread = PresenterThreadWorker(
            self.__close_session_using_other_thread)

        self.thread.when_started.connect(
            lambda: self.get_view().disable_gui(True))

        self.thread.error_found.connect(self.__handle_logout_exceptions)
        self.thread.error_found.connect(
            lambda: self.get_view().disable_gui(False))

        self.thread.finished_without_error.connect(
            lambda: self.get_view().stop_time_counter())
        self.thread.finished_without_error.connect(
            lambda: self._close_this_presenter())

        self.thread.start()

    def __close_session_using_other_thread(self, thread: PresenterThreadWorker):
        try:
            self.__nauta_client.logout()
            thread.finished_without_error.emit()
        except Exception as e:
            thread.error_found.emit(e)

    def __handle_logout_exceptions(self, exception: Exception):
        if isinstance(exception, NautaLogoutException):
            self.get_view().show_dialog_error_message(
                'No se pudo cerrar la sesión. Tal vez ya está cerrada, o no se encuentra conectado a la red.')
