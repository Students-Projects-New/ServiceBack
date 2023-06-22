from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from apps.app_user.api.serializers import UserTokenSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Si se quiere agregar algo al token
        # ...
        token['user'] = UserTokenSerializer(user).data

        return token

class MyTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        data = super(MyTokenRefreshSerializer, self).validate(attrs)
        
        # En caso de que se requiera personalizar el token de refresh
        #decoded_payload = token_backend.decode(data['access'], verify=True)
        #user_uid=decoded_payload['user_id']

        return data