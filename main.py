from easy_mvp.application_manager import ApplicationManager
from easy_mvp.intent import Intent
from presenter.main import MainPresenter
import view.ui.resources
import view.ui.icons_rc

app = ApplicationManager()
initial_intent = Intent(MainPresenter)
app.execute_app(initial_intent)