import os, uuid
from django.db import transaction, models
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from apps.app_project.models import Project
from apps.app_project.api.utils import MIME_TYPE
from apps.app_project.api.projects_stages.serializers import (
    ProjectStageSaveSerializer,
    ProjectStageSerializer,
    StageSaveFileSerializer,
    StageFileSerializer,
)
from apps.app_project.models import (
    Project, 
    StageFile,
    Stage,
    ProjectStage,
    File,
)
from apps.app_project.api.core import (
    CustomException, 
    DefaultSchema,
    TRUST
)

class ProjectStageView(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    def get(self, request: Request, pk_project: int):
        project_stages = ProjectStage.objects.filter(id_project=pk_project)
        serializer = ProjectStageSerializer(project_stages, many=True)
        return Response(serializer.data, status=200)

    def post(self, request: Request):
        serializer = ProjectStageSaveSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                project = Project.objects.get(id=serializer.validated_data['id_project'])

                stage = Stage()
                stage.id_user = request.user.id
                stage.name = serializer.validated_data['name']
                stage.description = (serializer.validated_data['description']
                                    if 'description' in serializer.validated_data else
                                    None)
                
                stage.save()

                project_stage = ProjectStage()
                project_stage.id_stage = stage
                project_stage.id_project = project

                project_stage.save()

            return Response(ProjectStageSerializer(project_stage).data, status=200)
        
        return Response(serializer.errors, status=400)
    
    def delete(self, request: Request, pk_stage_or_project: int):
        try:
            stage = Stage.objects.get(id=pk_stage_or_project)
            stage.delete()
        except Stage.DoesNotExist:
            raise CustomException('No se encontro la etapa del proyecto asociada')
        
        return Response(status=200)

class ProjectStageFileView(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    def get(self, request: Request, pk_stage: int):
        project_stage_files = StageFile.objects.filter(
            id_stage=pk_stage
        )
        serializer = StageFileSerializer(project_stage_files, context={'request': request}, many=True)
        return Response(serializer.data, status=200)

    def post(self, request: Request):
        serializer = StageSaveFileSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                stage = Stage.objects.get(
                    id=serializer.validated_data['id_stage']
                )

                uuid_file = str(uuid.uuid4())
                serializer.validated_data['uuid_file'] = uuid_file

                document = self._perform_create(request=request, uuid_file=uuid_file)
                
                project_stage_file = StageFile()
                project_stage_file.id_user = request.user.id
                project_stage_file.id_stage = stage
                project_stage_file.document = document
                project_stage_file.save()

                return Response(StageFileSerializer(project_stage_file, context={'request': request}).data, status=200)
        return Response(serializer.errors, status=400)

    def _perform_create(self, request: Request, uuid_file: str) -> File:
        filename = request.FILES['document'].name.split(".")

        if not filename[-1] in MIME_TYPE:
            raise CustomException(f'Extensión de archivo no valida, extensiones validas {*MIME_TYPE.keys(),}')

        request.FILES['document'].name = uuid_file + '.' + filename[-1]

        file = File()
        file.uuid_file = uuid_file
        file.name = "".join(filename[:-1])
        file.file = request.FILES['document']
        file.size = request.FILES['document'].size
        file.save()

        return file
