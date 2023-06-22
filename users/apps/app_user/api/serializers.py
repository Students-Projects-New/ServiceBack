from rest_framework import serializers
from apps.app_user.models import User, Rol, UserRol, Database, TypeDatabase
# serializers here

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = '__all__'

class UserRolSerialier(serializers.ModelSerializer):
    rol = serializers.SerializerMethodField('get_rol')

    def get_rol(self, user_rol: UserRol):
        rol_entity = Rol.objects.get(id=user_rol.rol_id.id)
        return RolSerializer(rol_entity).data

    class Meta:
        model = UserRol
        fields = ('rol',)

class UserTokenSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField('get_roles')
    
    def get_roles(self, user: User):
        roles_list =  UserRol.objects.filter(user_id=user.id)
        role_serializer = UserRolSerialier(roles_list, many=True).data

        res = []
        for data in role_serializer:
            rol = data['rol']
            res.append({'id': rol['id'], 'name': rol['name']})
        return res

    class Meta:
        model = User
        fields = (
            'id', 
            'username', 
            'first_name', 
            'last_name', 
            'roles',
            'is_active', 
            'email', 
            'google_id', 
            'picture',
            'has_sgbd_user',
        )


class ListUserByIdsSerializer(serializers.Serializer):
    id_users = serializers.ListField(child=serializers.IntegerField())

class EmailsSerializer(serializers.Serializer):
    emails = serializers.ListField(child=serializers.CharField())

class UserCardSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = (
            'id', 
            'first_name', 
            'last_name', 
            'picture',
        )

class CreateSGBDUserSerializer(serializers.Serializer):
    password = serializers.CharField()

class CreateDatabaseSerializer(serializers.Serializer):
    context = serializers.CharField()
    id_type = serializers.IntegerField()

class DatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Database
        fields = '__all__'

class TypeDatabaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeDatabase
        fields = '__all__'