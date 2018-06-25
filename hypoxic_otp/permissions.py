"""Custom Permissions for Hypoxic OTP"""
from rest_framework import permissions

from django_otp import user_has_device

from . import utils


class IsOtpVerified(permissions.BasePermission):
    """
    If user has verified TOTP device, require TOTP OTP.
    """
    message = "Your OTP device has not been verified. " \
              "Please verify it before continuing."

    def has_permission(self, request, view):
        if user_has_device(request.user):
            return utils.is_user_otp_verified(request)
        return True
