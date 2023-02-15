from easy_mvp.application_manager import ApplicationManager
from easy_mvp.intent import Intent
from presenter.main import MainPresenter


app = ApplicationManager()
initial_intent = Intent(MainPresenter)
app.execute_app(initial_intent)
