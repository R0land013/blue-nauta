from easy_mvp.abstract_presenter import AbstractPresenter
from view.opened_session import OpenedSessionView
from nautapy.nauta_api import NautaClient
from model.util.thread_worker import PresenterThreadWorker
from nautapy.exceptions import NautaLogoutException
from view.utils import show_action_confirmation_dialog


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
            go_to_main_view = show_action_confirmation_dialog(
                view=self.get_view(),
                title='No se pudo cerrar la sesión',
                message='Quizás ya esté cerrada o no se ecuentra conectado a la red. ¿Desea regresar a la vista principal?'
            )
            if go_to_main_view:
                self.get_view().stop_time_counter()
                self._close_this_presenter()
