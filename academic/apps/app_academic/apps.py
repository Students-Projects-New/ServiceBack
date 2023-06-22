from django.apps import AppConfig


class AppAcademicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_academic'

class CoreConfig(AppConfig):
    name = 'app_academic'
    label = 'app_academic'