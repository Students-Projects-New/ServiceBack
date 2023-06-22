from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from apps.app_user.models import User
from apps.app_user.services import handle_register
from .serializers import MyTokenObtainPairSerializer, MyTokenRefreshSerializer
from google.oauth2 import id_token
from google.auth.transport import requests
import os

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class MyTokenRefreshView(TokenRefreshView):
    serializer_class = MyTokenRefreshSerializer

def verify_google_token_and_get_info(token) -> dict:
    # Verify the token
    idinfo = id_token.verify_oauth2_token(token, requests.Request())
    if idinfo['aud'] not in [os.environ['CLIENT_WEB_ID'], os.environ['CLIENT_ANDROID_ID']]:
        raise ValueError('Could not verify audience.')

    return idinfo

def get_pair_token(user: User) -> dict:
    # Get pair token
    refresh = MyTokenObtainPairSerializer.get_token(user)
    access = refresh.access_token
    return {'access': str(access), 'refresh': str(refresh)}

class SignInUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        token = request.data['token']

        try:
            user_json = verify_google_token_and_get_info(token)
            
            # Check if user already exists
            user = User.objects.filter(google_id=user_json['sub']).exists()
            if not user:
                # Create user
                user = handle_register(user_json)
            else:
                user = User.objects.get(google_id=user_json['sub'])
        except Exception as e:
            return Response({'error': str(e)}, status=401)

        return Response(get_pair_token(user))
