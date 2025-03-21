from django.apps import AppConfig


class DummyDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dummy_api.dummy_data'

    def ready(self):
        from . import views
        views.initialize_data()