from django.urls import path
from apps.app_project.api.projects.api import (
    CreateProjectView, 
    DeployProjectView, 
    DeleteProjectView,
    DeleteWorkspaceView, 
    ListProjectView,
    CurrentLogProjectView,
    ValidateContextView,
    FindProject,
    ListProjectSubject,
    ListProjectDeployView,
    ListStatisticsView,
    FindStatusJobView
)

urlpatterns = [
    path('find_project/<int:id_project>', FindProject.as_view()),
    path('list_project/', ListProjectView.as_view()),
    path('list_project/<int:id_user>', ListProjectView.as_view()),
    path('create_project/', CreateProjectView.as_view()),
    path('deploy_project/', DeployProjectView.as_view()),
    path('delete_project/', DeleteProjectView.as_view()),
    path('delete_workspace/', DeleteWorkspaceView.as_view()),
    path('log_project/<int:id_project>/<str:type_log>', CurrentLogProjectView.as_view()),

    path('validate_context/<str:context>', ValidateContextView.as_view()),
    path('list_projects_subject/<int:id_subject_period>', ListProjectSubject.as_view()),

    path('list_deploys/<int:id_project>', ListProjectDeployView.as_view()),
    path('list_statistics/<int:id_project>', ListStatisticsView.as_view()),

    path('status_job/<int:id_job>', FindStatusJobView.as_view()),
]