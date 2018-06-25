"""Models for Hypoxic Service"""
import datetime
import logging

from copy import copy
from io import StringIO

from django.conf import settings
from django.db import models
from django.utils import timezone


LOGGER = logging.getLogger(__name__)


class Activity(models.Model):
    """Activity model"""
    user = models.IntegerField(null=True)
    name = models.CharField(max_length=100, db_index=True, blank=False)
    sport = models.ForeignKey('Sport', on_delete=models.PROTECT)
    route = models.ForeignKey('Route', on_delete=models.CASCADE)
    route_upload_status = models.CharField(default=None, max_length=20, null=True, blank=True)
    description = models.TextField(max_length=500, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_date = models.DateTimeField(auto_now=True, db_index=True)
    is_archived = models.BooleanField(default=False)


class Sport(models.Model):
    """Sport model"""
    name = models.CharField(max_length=100, db_index=True, blank=False)
    description = models.TextField(max_length=500, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_date = models.DateTimeField(auto_now=True, db_index=True)
    is_archived = models.BooleanField(default=False)


class Route(models.Model):
    """Route model"""
    name = models.CharField(max_length=100, db_index=True, blank=False)
    description = models.TextField(max_length=500, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_date = models.DateTimeField(auto_now=True, db_index=True)


class Lap(models.Model):
    """Lap model"""
    route = models.ForeignKey('Route', on_delete=models.PROTECT, related_name='route_laps')
    total_time_seconds = models.DecimalField(max_digits=20, decimal_places=2)
    distance_meters = models.DecimalField(max_digits=20, decimal_places=2)
    maximum_speed = models.DecimalField(max_digits=20, decimal_places=14)
    calories = models.IntegerField()
    average_heart_rate_bpm = models.IntegerField()
    maximum_heart_rate_bpm = models.IntegerField()
    intensity = models.CharField(max_length=30)
    trigger_method = models.CharField(max_length=30)
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_date = models.DateTimeField(auto_now=True, db_index=True)


class LapTrackPoint(models.Model):
    """Lap track point model"""
    lap = models.ForeignKey('Lap', on_delete=models.PROTECT, related_name='lap_track_points')
    time = models.DateTimeField()
    latitude_degrees = models.DecimalField(max_digits=16, decimal_places=14)
    longitude_degrees = models.DecimalField(max_digits=17, decimal_places=14)
    altitude_meters = models.DecimalField(max_digits=25, decimal_places=14)
    distance_meters = models.DecimalField(max_digits=20, decimal_places=14)
    heart_rate_bpm = models.IntegerField()
    speed = models.DecimalField(max_digits=20, decimal_places=14)
    run_cadence = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_date = models.DateTimeField(auto_now=True, db_index=True)
