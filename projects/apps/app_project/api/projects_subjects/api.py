from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.app_project.api.projects_subjects.serializers import ProjectSubjectSerializer
from apps.app_project.models import ProjectSubject
from apps.app_project.api.core import CustomException, TRUST

class ProjectSubjectView(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    def post(self, request: Request):
        subject_serializer = ProjectSubjectSerializer(data=request.data)
        if subject_serializer.is_valid(raise_exception=True):
            instance = subject_serializer.save()

            return Response(ProjectSubjectSerializer(instance).data)

class DeleteProjectSubjectView(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    def post(self, request: Request):
        subject_serializer = ProjectSubjectSerializer(data=request.data)
        if subject_serializer.is_valid(raise_exception=True):
            id_subject_period = id_subject_period = subject_serializer.validated_data['id_subject_period']
            list_subjects = ProjectSubject.objects.filter(
                id_project = subject_serializer.validated_data['id_project'],
            )
            if len(list_subjects) > 1:
                del_subject = None
                for subject in list_subjects:
                    if subject.id_subject_period == id_subject_period:
                        del_subject = subject
                if del_subject != None:
                    del_subject.delete()
                else:
                    raise CustomException("No se encontro materia asociada.")
            else:
                raise CustomException("El proyecto debe tener al menos una materia asociada.")
            return Response(status=200)