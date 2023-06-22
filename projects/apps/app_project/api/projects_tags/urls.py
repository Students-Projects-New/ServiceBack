from django.urls import path
from apps.app_project.api.projects_tags.api import (
    ListTagAreaView,
    ListTagProgrammingView,
    ProjectTagView,
)

urlpatterns = [
    path('list_tags_area/', ListTagAreaView.as_view()),
    path('list_tags_programming/', ListTagProgrammingView.as_view()),

    path('project_tag/', ProjectTagView.as_view()),
    path('project_tag/<int:pk>', ProjectTagView.as_view()),
]