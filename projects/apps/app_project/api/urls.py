from django.urls import path
from apps.app_project.api.projects import urls as projects_path
from apps.app_project.api.projects_files import urls as files_path
from apps.app_project.api.projects_stages import urls as stages_path
from apps.app_project.api.projects_tags import urls as tags_path
from apps.app_project.api.projects_variables import urls as variables_path
from apps.app_project.api.projects_collaborators import urls as collaborator_path
from apps.app_project.api.projects_subjects import urls as subject_path

urlpatterns = [
    *projects_path.urlpatterns,
    *files_path.urlpatterns,
    *stages_path.urlpatterns,
    *tags_path.urlpatterns,
    *variables_path.urlpatterns,
    *collaborator_path.urlpatterns,
    *subject_path.urlpatterns,
]
