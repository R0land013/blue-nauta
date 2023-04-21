from easy_mvp.application_manager import ApplicationManager
from easy_mvp.intent import Intent
from presenter.main import MainPresenter
from util.resources_path import resource_path

app = ApplicationManager(
    app_name='Blue Nauta',
    window_icon_path=resource_path('view/ui/assets/bluenauta.png'),
)
initial_intent = Intent(MainPresenter)
app.execute_app(initial_intent)
