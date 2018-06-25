"""Utilities for Hypoxic OTP"""
import calendar
import datetime

from django_otp import devices_for_user, models
from django_otp.plugins.otp_static import models as static_models
from django_otp.plugins.otp_totp import models as totp_models

from rest_framework_jwt import authentication, compat, utils
from rest_framework_jwt.settings import api_settings


jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def get_custom_jwt(user, device):
    """
    Generates a JWT for a validated OTP device.
    This resets the orig_iat timestamp, as user is re-validated.
    """

    payload = jwt_otp_payload_handler(user, device)
    return jwt_encode_handler(payload)


def get_user_static_device(user, confirmed=None):
    """
    Returns users' static device
    """
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, static_models.StaticDevice):
            return device


def get_user_totp_device(user, confirmed=None):
    """
    Returns users' TOTP device
    """
    devices = devices_for_user(user, confirmed=confirmed)
    for device in devices:
        if isinstance(device, totp_models.TOTPDevice):
            return device


def is_user_otp_verified(request):
    """
    Helper to determine if user has verified OTP.
    """
    auth = authentication.JSONWebTokenAuthentication()
    jwt_value = auth.get_jwt_value(request)
    if jwt_value is None:
        return False

    payload = utils.jwt_decode_handler(jwt_value)
    persistent_id = payload.get('otp_device_id')

    if persistent_id:
        device = models.Device.from_persistent_id(persistent_id)
        if device is not None and device.user_id != request.user.id:
            return False
        # Valid device in JWT
        return True
    return False


def jwt_otp_payload_handler(user, device=None):
    """
    Override default payload handler to optionally include OTP device
    """
    username = compat.get_username(user)

    payload = {
        'user_id': user.pk,
        'username': username,
        'exp': datetime.datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }

    # Include original issued at time for a brand new token, to allow token refresh
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = calendar.timegm(
            datetime.datetime.utcnow().utctimetuple()
        )

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER

    if user is not None and device is not None and (device.user_id == user.id and device.confirmed is True):
        payload['otp_device_id'] = device.persistent_id
    else:
        payload['otp_device_id'] = None

    return payload
