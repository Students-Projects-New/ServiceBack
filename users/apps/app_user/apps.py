from django.apps import AppConfig


class AppUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_user'

class CoreConfig(AppConfig):
    name = 'app_user'
    label = 'app_user'