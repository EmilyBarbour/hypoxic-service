"""Serializers for Hypoxic Service"""
from rest_framework_json_api import serializers

from . import models


class CurrentUserDefault(object):
    """
    Returns a default value of the id of the currently authenticated user when no input is provided. Assumes that
    the user has been authenticated via the Admin app
    """

    def set_context(self, serializer_field):
        """Called by rest_framework.fields.Field.get_default"""
        self.user = serializer_field.context['request'].user

    def __call__(self):
        return self.user.id


class ActivitySerializer(serializers.ModelSerializer):
    """DRF Serializer for the Activity model detail view"""
    user = serializers.HiddenField(default=CurrentUserDefault())

    included_serializers = {
        'sport': 'discovery_service.serializers.SportSerializer',
        'route': 'discovery_service.serializers.RouteSerializer',
    }

    class Meta:
        model = models.Activity
        resource_name = 'hypoxic-activity'
        fields = [
            'user',
            'id',
            'name',
            'sport',
            'route',
            'route_upload_status',
            'description',
            'created_date',
            'updated_date',
            'is_archived',
        ]

        extra_kwargs = {
            'created_date': {'read_only': True},
            'updated_date': {'read_only': True},
            'is_archived': {'read_only': True}
        }


class SportSerializer(serializers.ModelSerializer):
    """DRF Serializer for the Sport model detail view"""

    class Meta:
        model = models.Sport
        resource_name = 'hypoxic-sport'
        fields = [
            'id',
            'name',
            'description',
            'created_date',
            'updated_date',
            'is_archived',
        ]

        extra_kwargs = {
            'created_date': {'read_only': True},
            'updated_date': {'read_only': True},
            'is_archived': {'read_only': True}
        }


class RouteSerializer(serializers.ModelSerializer):
    """DRF Serializer for the Route model detail view"""

    included_serializers = {
        'route_laps': 'discovery_service.serializers.LapSerializer',
    }

    class Meta:
        model = models.Route
        resource_name = 'hypoxic-route'
        fields = [
            'id',
            'name',
            'description',
            'created_date',
            'updated_date',
            'route_laps',
        ]

        extra_kwargs = {
            'created_date': {'read_only': True},
            'updated_date': {'read_only': True},
            'route_laps': {'required': False},
        }


class LapSerializer(serializers.ModelSerializer):
    """DRF Serializer for the Lap model detail view"""

    included_serializers = {
        'route': 'discovery_service.serializers.RouteSerializer',
        'lap_track_points': 'discovery_service.serializers.LapTrackPointSerializer',
    }

    class Meta:
        model = models.Lap
        resource_name = 'hypoxic-lap'
        fields = [
            'id',
            'route',
            'total_time_seconds',
            'distance_meters',
            'maximum_speed',
            'calories',
            'average_heart_rate_bpm',
            'maximum_heart_rate_bpm',
            'intensity',
            'trigger_method',
            'created_date',
            'updated_date',
        ]

        extra_kwargs = {
            'created_date': {'read_only': True},
            'updated_date': {'read_only': True},
        }


class LapTrackPointSerializer(serializers.ModelSerializer):
    """DRF Serializer for the Lap Track Point model detail view"""

    included_serializers = {
        'lap': 'discovery_service.serializers.LapSerializer',
    }

    class Meta:
        model = models.LapTrackPoint
        resource_name = 'hypoxic-lap-track-point'
        fields = [
            'id',
            'lap',
            'latitude_degrees',
            'longitude_degrees',
            'altitude_meters',
            'distance_meters',
            'heart_rate_bpm',
            'speed',
            'run_cadence',
            'created_date',
            'updated_date',
        ]

        extra_kwargs = {
            'created_date': {'read_only': True},
            'updated_date': {'read_only': True},
        }
