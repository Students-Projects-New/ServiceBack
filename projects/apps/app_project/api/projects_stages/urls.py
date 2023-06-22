from django.urls import path
from apps.app_project.api.projects_stages.api import (
    ProjectStageView,
    ProjectStageFileView,
)

urlpatterns = [
    path('project_stage/', ProjectStageView.as_view()),
    path('project_stage/<int:pk_project>', ProjectStageView.as_view()),

    path('project_stage_file/', ProjectStageFileView.as_view()),
    path('project_stage_file/<int:pk_stage>', ProjectStageFileView.as_view()),
]