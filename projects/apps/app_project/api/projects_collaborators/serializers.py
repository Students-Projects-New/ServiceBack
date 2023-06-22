from rest_framework import serializers
from apps.app_project.models import ProjectCollaborator

class ProjectCollaboratorSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectCollaborator
        fields = '__all__'
