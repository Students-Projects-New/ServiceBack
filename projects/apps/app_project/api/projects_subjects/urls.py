from django.urls import path
from apps.app_project.api.projects_subjects.api import ProjectSubjectView, DeleteProjectSubjectView

urlpatterns = [
    path('save_project_subject/', ProjectSubjectView.as_view()),
    path('delete_project_subject/', DeleteProjectSubjectView.as_view()),
]