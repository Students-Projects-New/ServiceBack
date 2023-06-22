from django.apps import AppConfig


class AppProjectConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_project'

class CoreConfig(AppConfig):
    name = 'app_project'
    label = 'app_project'