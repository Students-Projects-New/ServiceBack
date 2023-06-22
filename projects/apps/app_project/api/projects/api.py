import os, uuid, typing, json, uuid
from django.db import transaction
from django.db.models import Q
from docker_app.automatization import update_logs, delete_workspace
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from apps.app_project.api.utils import MIME_TYPE
from apps.app_project.api.projects.serializers import (
    ProjectSerializer,
    DeployProjectSerializer,
    ListProjectByTagSerializer
)
from apps.app_project.models import (
    Project, 
    ProjectTag,
    StageFile,
    ProjectStage,
    EnvironmentVariable, 
    TypeLog,
    ProjectSubject,
    ProjectCollaborator,
    TypeJob,
    Job,
    ProjectDeploy,
    ProjectStatistics,
    Status
)
from apps.app_project.api.core import (
    CustomException, 
    DefaultSchema,
    TRUST
)
from apps.app_project.api.projects.serializers import (
    DeleteProjectSerializer, 
    DeleteWorkspaceSerializer,
    JobSerializer,
    DeployProjectSerializer,
    ProjectStatisticsSerializer,
    ProjectDeploySerializer
)
from apps.app_project.service_api import ServiceApi, ServiceType
from apps.app_project.cipher import AESCipher

class FindProject(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )
    schema = DefaultSchema()

    def get(self, request: Request, id_project: int):
        try:
            project = Project.objects.get(id=id_project)
            return Response(ProjectSerializer(project, context={'request': request}).data, status=200)
        except Project.DoesNotExist:
            raise CustomException("No se encontro proyecto asociado")

class ListProjectView(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )
    schema = DefaultSchema()

    def post(self, request: Request, id_user: int = 0):
        projects_serializer: ProjectSerializer = None
        if 'id_tags' in request.data:
            projects_serializer = self._perform_by_tag(request=request)
        elif id_user != 0:
            projects_serializer = self._perform_by_user(request=request, id_user=id_user)
        else:
            projects_serializer = self._perform_by_all(request=request)

        return Response(projects_serializer.data)

    def _perform_by_all(self, request: Request) -> ProjectSerializer:
        projects = Project.objects.all()
        return ProjectSerializer(projects, context={'request': request}, many=True)

    def _perform_by_user(self, request: Request, id_user: int) -> ProjectSerializer:
        projects = Project.objects.filter(
            id_user = id_user
        )
        projects_collabs = ProjectCollaborator.objects.filter(
            id_collaborator=id_user
        )

        list_project = []
        for project in projects:
            list_project.append(project)
        for project_collab in projects_collabs:
            list_project.append(project_collab.id_project)

        return ProjectSerializer(list_project, context={'request': request}, many=True)
    
    def _perform_by_tag(self, request: Request) -> ProjectSerializer:
        serializer = ListProjectByTagSerializer(data=request.data)
        if serializer.is_valid():
            tags_id = serializer.validated_data['id_tags']
            print(tags_id)
            project_tags = (ProjectTag.objects
                                .filter(id_tag__in=tags_id)
                                .values('id_project'))
            print(project_tags, type(project_tags))
            _list_project_tags = [project_tag['id_project_id'] for project_tag in project_tags.values()]
            projects = Project.objects.filter(id__in=_list_project_tags)
            return ProjectSerializer(projects, context={'request': request}, many=True)

        return ProjectSerializer([], many=True)
    
class ListProjectSubject(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )
    schema = DefaultSchema()

    def get(self, request: Request, id_subject_period: int):
        try:
            subject_projects = ProjectSubject.objects.filter(
                id_subject_period = id_subject_period
            )
            list_projects: typing.List[Project] = [
                subject_project.id_project for subject_project in subject_projects
            ]

            return Response(ProjectSerializer(
                list_projects, 
                context={'request': request}, 
                many=True
            ).data, status=200)

        except Project.DoesNotExist:
            raise CustomException("No se encontro proyecto asociado")
    
class CreateProjectView(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )
    schema = DefaultSchema()

    def post(self, request: Request):
        project_serializer = ProjectSerializer(data=request.data)
        if project_serializer.is_valid(raise_exception=True):
            uuid_image = str(uuid.uuid4())
            project_serializer.validated_data['uuid_image'] = uuid_image

            with transaction.atomic():
                self._perform_create(request=request, uuid_image=uuid_image)
                project = project_serializer.save()
                self._post_create(request=request, instance=project)

            return Response(ProjectSerializer(project, context={'request': request}).data, status=200)
        return Response(project_serializer.errors, status=400)

    def _post_create(self, request: Request, instance: Project):
        project_subject = ProjectSubject()
        project_subject.id_project = instance
        project_subject.id_subject_period = request.data['subject_period']
        project_subject.save()

    def _perform_create(self, request: Request, uuid_image: str):
        if 'subject_period' not in request.data:
            try:
                request.data['subject_period'] = int(request.data['subject_period'])
            except:
                raise CustomException("El campo materia no valido, por favor revise los datos")

        if 'image' in request.FILES:
            ext = request.FILES['image'].name.split(".")[-1]

            if not ext.lower() in MIME_TYPE:
                raise CustomException(f'Extensión de archivo no valida, extensiones validas {*MIME_TYPE.keys(),}')

            request.FILES['image'].name = uuid_image + '.' + ext

class DeployProjectView(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )
    schema = DefaultSchema()

    def _get_last_deploy(self, project: Project) -> ProjectDeploy:
        fl_project = Q(id_project=project.id)
        fl_status_vig = Q(status=Status.VIG.value)
        fl_status_run = Q(status=Status.RUN.value)
        return (ProjectDeploy.objects
            .filter(fl_project & (fl_status_run | fl_status_vig))
            .first()
        )

    def post(self, request):
        deploy_serializer = DeployProjectSerializer(data=request.data)
        if deploy_serializer.is_valid(raise_exception=True):
            try:
                project = Project.objects.get(
                    id_user = deploy_serializer.data['id_user'],
                    id = deploy_serializer.data['id_project']
                )
            except Project.DoesNotExist as e:
                raise CustomException("No se encontro proyecto asociado")

            has_deploy = self._get_last_deploy(project=project)
            if has_deploy != None:
                raise CustomException(
                    "Ya se encuentra un despliegue {}".format(
                        "ejecutandose." if has_deploy.status == Status.RUN.value else "por ejecutar."
                    )
                )

            var_envs = EnvironmentVariable.objects.filter(
                id_project_id = project.id
            )

            dict_var = {
                var_env.name_var: var_env.value_var
                for var_env in var_envs
            } 

            dinamico = {
                "context": project.context,
                "env_var": dict_var,
                "port_container": project.port_container,
                "static_path": project.static_path,
                "url": project.url,
            }

            with transaction.atomic():
                guid = str(uuid.uuid4())

                project.guid = guid
                project.save()

                deploy_model = ProjectDeploy()
                deploy_model.id_project = project
                deploy_model.id_user_deploy =  deploy_serializer.data['id_user_deploy']
                deploy_model.guid = guid
                deploy_model.save()

                job = Job()
                job.guid = guid
                job.dinamico = json.dumps(dinamico)
                job.message = ''
                job.status = 'VIG'
                job.type = TypeJob.DEPLOY.value
                job.progress = 0
                job.save()

            return Response(JobSerializer(job).data, status=200)
        return Response(deploy_serializer.errors, status= 400)

class CurrentLogProjectView(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    def get(self, request, id_project, type_log):
        try:
            project = Project.objects.get(
                id = id_project
            )
        except Project.DoesNotExist as e:
            raise CustomException("No se encontro proyecto asociado")

        type_log = TypeLog.get(type_log=type_log)

        try:
            if type_log == TypeLog.CONT:
                update_logs(project.context)

            base = os.environ["STUDENTS_PROJECTS_DEPLOY_ROOT"]
            path = os.path.join(base, project.context)
            path_log = os.path.join(path, type_log.value)

            return Response(self._parse_logs(path_log=path_log), status=200)
        except:
            raise CustomException("No se encontraron logs para el proyecto")
    
    def _parse_logs(self, path_log: str) -> typing.List[typing.Dict[str, str]]:
        log_lines = []

        with open(path_log, 'r') as file_log:
            lines = file_log.readlines()

        for line in lines:
            log_lines.append({"message": line})
        
        return log_lines

class DeleteProjectView(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    def post(self, request):
        serializer = DeleteProjectSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                try:
                    project = Project.objects.get(
                        id_user = serializer.data['id_user'],
                        id = serializer.data['id_project']
                    )
                except Project.DoesNotExist as e:
                    raise CustomException("No se encontro proyecto asociado")

                DeleteWorkspaceView.delete_workspace(project)
                self._perform_destroy(project=project)
                project.delete()

            return Response(status=200)
        return Response(serializer.errors, status=400)
    
    def _perform_destroy(self, project: Project) -> None:
        #any process before delete
        os.remove(project.image.path)
        project_stages = ProjectStage.objects.filter(id_project=project.id)
        for project_stage in project_stages:
            stage_files = StageFile.objects.filter(id_stage=project_stage.id_stage.id)
            for stage_file in stage_files:
                os.remove(stage_file.document.file.path)
            project_stage.id_stage.delete()

class DeleteWorkspaceView(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    def post(self, request):
        workspace_serializer = DeleteWorkspaceSerializer(data=request.data)
        if workspace_serializer.is_valid(raise_exception=True):

            try:
                project = Project.objects.get(
                    id_user = workspace_serializer.data['id_user'],
                    id = workspace_serializer.data['id_project']
                )
            except Project.DoesNotExist as e:
                raise CustomException("No se encontro proyecto asociado")

            project.running = False
            project.save()
            DeleteWorkspaceView.delete_workspace(project)

            return Response(status=200)
        return Response(workspace_serializer.errors, status=400)
    
    @staticmethod
    def delete_workspace(project: Project) -> None:
        delete_workspace(
            context=project.context,
            static=project.static_path.split("/")[-1]
        )

class ValidateContextView(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    def get(self, request: Request, context: str):
        project = Project.objects.filter(context=context).first()
        return Response({'exist': project != None}, status=200)

class ListProjectDeployView(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    def get(self, request: Request, id_project: int):
        deploys = ProjectDeploy.objects.filter(id_project=id_project)
        deploys_serializers = ProjectDeploySerializer(deploys, many=True)
        return Response(deploys_serializers.data, status=200)

class ListStatisticsView(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    def get(self, request: Request, id_project: int):
        statistics = ProjectStatistics.objects.filter(id_project=id_project)
        statistics_serializer = ProjectStatisticsSerializer(statistics, many=True)
        return Response(statistics_serializer.data, status=200)

class FindStatusJobView(APIView):
    permission_classes = (
        [AllowAny] 
        if TRUST else 
        [IsAuthenticated]
    )

    def get(self, request: Request, id_job: int):
        try:
            job = Job.objects.get(id=id_job)
        except Job.DoesNotExist:
            raise CustomException("No se encontro job asociado")
        job_serializer = JobSerializer(job)
        return Response(job_serializer.data, status=200)
