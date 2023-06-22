from django.db import transaction
from apps.app_user.models import User, UserRol

def handle_register(user_json: dict) -> User:
    with transaction.atomic():
        user = User()
        user.google_id = user_json['sub']
        user.first_name = user_json['given_name']
        user.last_name = user_json['family_name']
        user.email = user_json['email']
        user.username = user_json['email']
        user.picture = user_json['picture']
        user.save()

        user_rol = UserRol()
        user_rol.user_id = user
        user_rol.save()

    return user