from rest_framework import serializers
from apps.app_project.models import File

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
        extra_kwargs = {'uuid_image': {'required': False}}
        read_only_fields = ['uuid_image']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = '__all__'
