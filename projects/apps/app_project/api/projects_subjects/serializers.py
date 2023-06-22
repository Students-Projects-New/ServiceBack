from rest_framework import serializers
from apps.app_project.models import ProjectSubject

class ProjectSubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectSubject
        fields = '__all__'
