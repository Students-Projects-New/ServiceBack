from rest_framework import serializers
from apps.app_project.models import (
    Stage,
    StatusStage,
    ProjectStage,
    StageFile
)
from apps.app_project.api.projects_files.serializers import FileSerializer

class ProjectStageSaveSerializer(serializers.Serializer):
    id_project = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    description = serializers.CharField()

    class Meta:
        extra_kwargs = {'description': {'required': False}}

class StatusStageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusStage
        fields = '__all__'

class StageSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField(method_name='get_status')
    files = serializers.SerializerMethodField(method_name='get_files')

    def get_status(self, stage: Stage):
        return StatusStageSerializer(stage.status).data

    def get_files(self, stage: Stage):
        _stage_files = StageFile.objects.filter(id_stage=stage.id)
        _stages_files_list = []
        for _stage_file in _stage_files:
            _stages_files_list.append(FileSerializer(_stage_file.document, context=self.context).data)
        return _stages_files_list

    class Meta:
        model = Stage
        fields = '__all__'

class ProjectStageSerializer(serializers.ModelSerializer):
    id_stage = serializers.SerializerMethodField(method_name='get_stage')

    def get_stage(self, project_stage: ProjectStage):
        return StageSerializer(project_stage.id_stage).data

    class Meta:
        model = ProjectStage
        fields = '__all__'

class StageSaveFileSerializer(serializers.Serializer):
    id_stage = serializers.IntegerField()
    document = serializers.FileField()

class StageFileSerializer(serializers.ModelSerializer):
    document = serializers.SerializerMethodField(method_name='get_document')

    def get_document(self, stage_file: StageFile):
        return FileSerializer(stage_file.document, context=self.context).data

    class Meta:
        model = StageFile
        fields = '__all__'
        