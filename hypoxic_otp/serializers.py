import calendar
import datetime

from django.utils.translation import ugettext as _
from rest_framework import serializers

from rest_framework_jwt import serializers as jwt_serializers
from rest_framework_jwt.settings import api_settings

from . import utils


jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER


class RefreshJSONWebTokenSerializer(jwt_serializers.VerificationBaseSerializer):
    """
    Refresh an access token.  Include OTP device in payload
    """

    def validate(self, attrs):
        """Overide validate to include OTP device param"""
        token = attrs['token']

        payload = self._check_payload(token=token)
        user = self._check_user(payload=payload)
        # Get and check 'orig_iat'
        orig_iat = payload.get('orig_iat')
        # Get TOTP device for user
        device = utils.get_user_totp_device(user)

        if orig_iat:
            # Verify expiration
            refresh_limit = api_settings.JWT_REFRESH_EXPIRATION_DELTA

            if isinstance(refresh_limit, datetime.timedelta):
                refresh_limit = (refresh_limit.days * 24 * 3600 +
                                 refresh_limit.seconds)

            expiration_timestamp = orig_iat + int(refresh_limit)
            now_timestamp = calendar.timegm(datetime.datetime.utcnow().utctimetuple())

            if now_timestamp > expiration_timestamp:
                msg = _('Refresh has expired.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('orig_iat field is required.')
            raise serializers.ValidationError(msg)

        new_payload = jwt_payload_handler(user, device)
        new_payload['orig_iat'] = orig_iat

        return {
            'token': jwt_encode_handler(new_payload),
            'user': user
        }
