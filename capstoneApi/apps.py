from django.apps import AppConfig


class CapstoneapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'capstoneApi'

    def ready(self) -> None:
        from jobscheduler.scheduler import start
        start()
