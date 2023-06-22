from django.urls import path
from apps.app_academic.api.api import SubjectView, SubjectPeriodView, SubjectStudentView, SubjectPeriodDetailView,SubjectStudentDetailView,SubjectsStudentsPeriod,SubjectPeriodDetailByIdView

urlpatterns = [
    path('subjects/',SubjectView.as_view()),
    path('subjects/<int:id_subject>/',SubjectView.as_view()),
    path('subjectsPeriod/',SubjectPeriodView.as_view()),
    path('subjectsPeriod/<int:id_subject_period>/',SubjectPeriodView.as_view()),
    path('subjectsStudent/',SubjectStudentView.as_view()),
    path('subjectsStudent/<int:id_subject_student>',SubjectStudentView.as_view()),
    path('subjectsPeriodDetail/<int:id_teacher>',SubjectPeriodDetailView.as_view()),
    path('subjectStudentDetailView/<int:id_student>',SubjectStudentDetailView.as_view()),
    path('subjectStudentPeriod/<int:id_subject_period>',SubjectsStudentsPeriod.as_view()),
    path('subjectsPeriodDetailById/<int:id_period>',SubjectPeriodDetailByIdView.as_view()),
]