from rest_framework import serializers
from apps.app_project.api.projects.docs import (
    ProjectDocs, 
    DeployProjectDocs,
    DeleteWorkspaceProjectDocs
)
from apps.app_project.models import (
    Project,
    ProjectTag,
    ProjectStage,
    ProjectCollaborator,
    ProjectSubject,
    Job,
    ProjectDeploy,
    ProjectStatistics,
)

from apps.app_project.api.projects_stages.serializers import StageSerializer
from apps.app_project.api.projects_tags.serializers import TagSerializer

class ProjectSerializer(serializers.ModelSerializer, ProjectDocs):
    tags = serializers.SerializerMethodField(method_name='get_tags')
    stages = serializers.SerializerMethodField(method_name='get_stages')
    collaborators = serializers.SerializerMethodField(method_name='get_collaborators')
    subjects_period = serializers.SerializerMethodField(method_name='get_subjects')

    def get_tags(self, project: Project):
        _tags_project = ProjectTag.objects.filter(id_project=project.id)
        _tags_list = []
        for tag in _tags_project:
            _tags_list.append({
                'id_project_tag': tag.id, 
                'tag': TagSerializer(tag.id_tag).data
            })
        return _tags_list

    def get_stages(self, project: Project):
        _stages_project = ProjectStage.objects.filter(id_project=project.id)
        _stages_list = []
        for _stage in _stages_project:
            _stages_list.append(StageSerializer(_stage.id_stage, context=self.context).data)
        return _stages_list

    def get_collaborators(self, project: Project):
        _collaborators_project = ProjectCollaborator.objects.filter(id_project=project.id)
        _collaborators_list = []
        for _collaborator in _collaborators_project:
            _collaborators_list.append(_collaborator.id_collaborator)
        return _collaborators_list

    def get_subjects(self, project: Project):
        _subjects_project = ProjectSubject.objects.filter(id_project=project.id)
        _subjects_list = []
        for _subjects in _subjects_project:
            _subjects_list.append(_subjects.id_subject_period)
        return _subjects_list

    class Meta:
        model = Project
        fields = '__all__'
        read_only_fields = ['uuid_image']

class ListProjectByTagSerializer(serializers.Serializer):
    id_tags = serializers.ListField(
        child = serializers.IntegerField()
    )

    class Meta:
        extra_kwargs = {'id_tags': {'required': False}}

class DeployProjectSerializer(serializers.Serializer, DeployProjectDocs):
    id_user = serializers.IntegerField(required=True)
    id_user_deploy = serializers.IntegerField(required=True)
    id_project = serializers.IntegerField(required=True)

    class Meta:
        fields = '__all__'

class DeleteSerializer(serializers.Serializer, DeleteWorkspaceProjectDocs):
    id_user = serializers.IntegerField(required=True)
    id_project = serializers.IntegerField(required=True)

    class Meta:
        fields = '__all__'

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = (
            'id',
            'guid',
            'type',
            'message',
            'status',
            'progress',
            'created_at',
            'updated_at',
        )

class ProjectDeploySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDeploy
        fields = '__all__'

class ProjectStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectStatistics
        fields = '__all__'

class DeleteWorkspaceSerializer(DeleteSerializer):
    pass

class DeleteProjectSerializer(DeleteSerializer):
    pass
