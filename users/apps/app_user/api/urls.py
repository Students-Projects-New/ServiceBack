from django.contrib import admin
from django.urls import path
from apps.app_user.api.api import (
    ListUsersById, 
    ListUsersIdsByEmails, 
    UpdateRolDocente,
    ListTypeDatabase,
    CreateSGBDUser,
    CreateDatabase,
    ListDatabase,
    DeleteDatabase,
    SearchDatabase
)

urlpatterns = [
    path('list_users_by_ids/', ListUsersById.as_view()),
    path('get_ids_by_email/', ListUsersIdsByEmails.as_view()),
    path('update_to_teacher/', UpdateRolDocente.as_view()),
    path('list_types_database/', ListTypeDatabase.as_view()),
    path('create_user_sgbd/', CreateSGBDUser.as_view()),
    path('create_database/', CreateDatabase.as_view()),
    path('list_database/', ListDatabase.as_view()),
    path('delete_database/<int:pk_db>', DeleteDatabase.as_view()),
    path('search_database/<str:context>', SearchDatabase.as_view()),
]
