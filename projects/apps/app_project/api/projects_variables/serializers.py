from rest_framework import serializers
from apps.app_project.models import EnvironmentVariable

class EnvironmentVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvironmentVariable
        fields = '__all__'
        extra_kwargs = {
            'name_var': {'required': True},
            'value_var': {'required': True},
        }