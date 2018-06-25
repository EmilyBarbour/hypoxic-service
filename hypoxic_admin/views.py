"""Views for Hypoxic Admin"""
import datetime
import requests
import uuid

from djoser import serializers as djoser_serializers, views as djoser_views

from rest_framework import permissions, status, views
from rest_framework.response import Response

from rest_framework_jwt import views as jwt_views
from rest_framework_jwt.settings import api_settings

from hypoxic_otp import (
    permissions as otp_permissions,
    serializers as otp_serializers,
    utils as otp_utils,
)
from . import models


jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class HypoxicUserView(djoser_views.UserView):
    """
    Default Djoser view + IsOtpVerified permission.
    """
    model = models.HypoxicUser
    queryset = models.HypoxicUser.objects.all()
    serializer_class = djoser_serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated, otp_permissions.IsOtpVerified]


class HypoxicUserActivateView(views.APIView):
    """User facing activation view"""
    queryset = models.HypoxicUser.objects.all()

    def get(self, request, uid, token):
        """Override get"""
        scheme = 'https://' if request.is_secure() else 'http://'
        netloc = request.get_host()
        path = '/api/user/activate/'
        url = f'{scheme}{netloc}{path}'
        payload = {
            'uid': uid,
            'token': token,
        }
        result = requests.post(url, data=payload)
        content = result.text
        return Response(content)


class HypoxicUserDeleteView(djoser_views.UserDeleteView):
    """
    Default Djoser view + IsOtpVerified permission.
    """
    queryset = models.HypoxicUser.objects.all()
    serializer_class = djoser_serializers.UserDeleteSerializer
    permission_classes = [permissions.IsAuthenticated, otp_permissions.IsOtpVerified]


class HypoxicUserLogoutView(views.APIView):
    """
    Logout all sessions for a given user
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """override post"""
        user = request.user
        user.jwt_secret = uuid.uuid4()
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HypoxicUserRefreshJSONWebToken(jwt_views.JSONWebTokenAPIView):
    """
    Default JWT RefreshJSONWebToken view + Serializer overriden
    to retain otp_device_id
    """
    serializer_class = otp_serializers.RefreshJSONWebTokenSerializer


class HypoxicPasswordResetView(djoser_views.PasswordResetView):
    """
    Default Djoser view + IsOtpVerified permission.
    """
    model = models.HypoxicUser
    queryset = models.HypoxicUser.objects.all()
    permission_classes = [permissions.IsAuthenticated, otp_permissions.IsOtpVerified]


class HypoxicPasswordResetConfirmView(djoser_views.PasswordResetConfirmView):
    """
    Default Djoser view + IsOtpVerified permission.
    """
    model = models.HypoxicUser
    queryset = models.HypoxicUser.objects.all()
    permission_classes = [permissions.IsAuthenticated, otp_permissions.IsOtpVerified]
