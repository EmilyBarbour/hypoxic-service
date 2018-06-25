import uuid

from django_otp import devices_for_user
from django_otp.plugins.otp_static import models as static_models

from rest_framework import permissions, response, status, views

from hypoxic_otp import utils
from hypoxic_otp import permissions as otp_permissions


class StaticCreateView(views.APIView):
    """
    Create static recovery codes
    """
    permission_classes = [permissions.IsAuthenticated, otp_permissions.IsOtpVerified]
    number_of_static_tokens = 5

    def get(self, request):
        """override get"""
        device = utils.get_user_static_device(request.user)
        if not device:
            device = static_models.StaticDevice.objects.create(user=request.user, name="Static")

        device.token_set.all().delete()
        tokens = []
        for _ in range(self.number_of_static_tokens):
            token = static_models.StaticToken.random_token()
            device.token_set.create(token=token)
            tokens.append(token.decode('utf-8'))

        return response.Response(tokens, status=status.HTTP_201_CREATED)


class StaticVerifyView(views.APIView):
    """
    Verify static codes
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, token):
        user = request.user
        device = utils.get_user_static_device(user)
        if device is not None and device.verify_token(str.encode(token)):
            token = utils.get_custom_jwt(user, device)
            return response.Response({'token': token}, status=status.HTTP_201_CREATED)
        return response.Response(status=status.HTTP_400_BAD_REQUEST)


class TOTPCreateView(views.APIView):
    """
    Setup a new TOTP device
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        device = utils.get_user_totp_device(user)
        if not device:
            device = user.totpdevice_set.create(confirmed=False)
        url = device.config_url
        return response.Response(url, status=status.HTTP_201_CREATED)


class TOTPDeleteView(views.APIView):
    """
    Delete a TOTP device
    """
    permission_classes = [permissions.IsAuthenticated, otp_permissions.IsOtpVerified]

    def post(self, request):
        """override post with TOTP verification"""
        user = request.user
        devices = devices_for_user(user)
        for device in devices:
            device.delete()
        user.jwt_secret = uuid.uuid4()
        user.save()
        token = utils.get_custom_jwt(user, None)
        return response.Response({'token': token}, status=status.HTTP_200_OK)


class TOTPVerifyView(views.APIView):
    """
    Verify/enable a TOTP device
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, token):
        """override post with TOTP verification"""
        user = request.user
        device = utils.get_user_totp_device(user)
        if device is not None and device.verify_token(token):
            if not device.confirmed:
                device.confirmed = True
                device.save()
            token = utils.get_custom_jwt(user, device)
            return response.Response({'token': token}, status=status.HTTP_201_CREATED)
        return response.Response(status=status.HTTP_400_BAD_REQUEST)
