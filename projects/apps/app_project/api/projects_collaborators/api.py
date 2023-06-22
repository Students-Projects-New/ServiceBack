from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.app_project.api.projects_collaborators.serializers import ProjectCollaboratorSerializer
from apps.app_project.models import ProjectCollaborator
from apps.app_project.api.core import CustomException, TRUST

class ProjectCollaboratorView(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    def post(self, request: Request):
        collaborator_serializer = ProjectCollaboratorSerializer(data=request.data)
        if collaborator_serializer.is_valid(raise_exception=True):
            instance = collaborator_serializer.save()

            return Response(ProjectCollaboratorSerializer(instance).data)

class DeleteProjectCollaboratorView(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )
    
    def post(self, request: Request):
        collaborator_serializer = ProjectCollaboratorSerializer(data=request.data)
        if collaborator_serializer.is_valid(raise_exception=True):
            try:
                ProjectCollaborator.objects.filter(
                    id_project = collaborator_serializer.validated_data['id_project'],
                    id_collaborator = collaborator_serializer.validated_data['id_collaborator']
                ).delete()
            except ProjectCollaborator.DoesNotExist:
                raise CustomException("No se encontro colaborador asociado.")

            return Response(status=200)