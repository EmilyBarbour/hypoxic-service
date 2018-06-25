"""DRF Views for Hypoxic Service"""
from rest_framework import (
    viewsets,
)

from . import models, serializers

"""
TODO:
 - Filters

"""


class ActivityViewSet(viewsets.ModelViewSet):
    """DRF Viewset for Activity"""
    queryset = models.Activity.objects.all()
    serializer_class = serializers.ActivitySerializer


class SportViewSet(viewsets.ModelViewSet):
    """DRF Viewset for Sport"""
    queryset = models.Sport.objects.all()
    serializer_class = serializers.SportSerializer


class RouteViewSet(viewsets.ModelViewSet):
    """DRF Viewset for Route"""
    queryset = models.Route.objects.all()
    serializer_class = serializers.RouteSerializer


class LapViewSet(viewsets.ModelViewSet):
    """DRF Viewset for Lap"""
    queryset = models.Lap.objects.all()
    serializer_class = serializers.LapSerializer


class LapTrackPointViewSet(viewsets.ModelViewSet):
    """DRF Viewset for Lap"""
    queryset = models.LapTrackPoint.objects.all()
    serializer_class = serializers.LapTrackPointSerializer
