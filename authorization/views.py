from django.contrib.auth.models import User
from rest_framework.generics import (
    CreateAPIView,
    UpdateAPIView
)
from rest_framework.permissions import (
    IsAuthenticated,
    AllowAny
)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from authorization.serializers import (
    RegisterSerializer,
    ChangePasswordSerializer,
    UpdateProfileSerializer,
)


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer


class UpdateProfileView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateProfileSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response("Successful Logout", status=status.HTTP_205_RESET_CONTENT)
        except KeyError:
            return Response({
                'refresh': 'Invalid refresh token'
            }, status=status.HTTP_400_BAD_REQUEST)
