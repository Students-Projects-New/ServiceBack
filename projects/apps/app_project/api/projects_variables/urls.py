from django.urls import path
from apps.app_project.api.projects_variables.api import (
    CreateEnvironmentVariableView,
    ListEnvironmentVariableView,
)

urlpatterns = [
    path('list_env/<int:id_user>/<int:id_project>', ListEnvironmentVariableView.as_view()),
    path('create_env/', CreateEnvironmentVariableView.as_view()),
    path('delete_env/<int:pk_env>', CreateEnvironmentVariableView.as_view()),
]
