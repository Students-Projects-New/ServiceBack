from django.urls import path
from apps.app_project.api.projects_files.api import GetFileProjectView

urlpatterns = [
    path('media/images/<str:uuid_image>', GetFileProjectView.as_view()),
    path('media/files/<str:uuid_image>', GetFileProjectView.as_view()),
]