"""URL Routes for Hypoxic Service"""
from django.urls import include, path, re_path

from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter(trailing_slash=True)
router.register('activity', views.ActivityViewSet, base_name='activity')
router.register('sport', views.SportViewSet)
router.register('route', views.RouteViewSet)
router.register('lap', views.LapViewSet)
router.register('lap-track-point', views.LapTrackPointViewSet)

urlpatterns = [
    re_path(r'^api/hypoxic/v1/', include(router.urls)),
]
