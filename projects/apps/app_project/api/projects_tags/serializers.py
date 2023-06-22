from rest_framework import serializers
from apps.app_project.models import (
    TypeTag,
    Tag,
    ProjectTag,
)

class TypeTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeTag
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    type_tag = serializers.SerializerMethodField(method_name='get_type')

    def get_type(self, tag: Tag):
        return TypeTagSerializer(tag.type_tag).data

    class Meta:
        model = Tag
        fields = '__all__'

class ProjectTagSerializer(serializers.ModelSerializer):
    tag = serializers.SerializerMethodField(method_name='get_tag')

    def get_tag(self, project_tag: ProjectTag):
        serializer = TagSerializer(project_tag.id_tag)
        return serializer.data

    class Meta:
        model = ProjectTag
        fields = '__all__'
