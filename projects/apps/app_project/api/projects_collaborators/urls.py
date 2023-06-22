from django.urls import path
from apps.app_project.api.projects_collaborators.api import ProjectCollaboratorView, DeleteProjectCollaboratorView

urlpatterns = [
    path('save_project_collaborator/', ProjectCollaboratorView.as_view()),
    path('delete_project_collaborator/', DeleteProjectCollaboratorView.as_view()),
]