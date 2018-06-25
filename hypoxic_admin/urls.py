"""URL Routes for Hypoxic Admin"""
from django.conf.urls import re_path
from djoser import views as djoser_views
from rest_framework_jwt import views as jwt_views

from . import views


"""
TODO:
 - Token verification
 - Username change
 - Password change
"""

urlpatterns = [
    re_path(r'^user/view/$', views.HypoxicUserView.as_view(), name='user-view'),

    re_path(r'^user/create/$', djoser_views.UserCreateView.as_view(), name='user-create'),
    re_path(
        r'^user/activate/(?P<uid>[\w-]+)/(?P<token>[\w-]+)/$',
        views.HypoxicUserActivateView.as_view(),
        name='user-activate-display'
    ),
    re_path(r'^user/activate/$', djoser_views.ActivationView.as_view(), name='user-activate'),
    re_path(r'^user/delete/$', views.HypoxicUserDeleteView.as_view(), name='user-delete'),

    re_path(r'^user/login/$', jwt_views.obtain_jwt_token, name='user-login'),
    re_path(r'^user/login/refresh/$', views.HypoxicUserRefreshJSONWebToken.as_view(), name='user-login-refresh'),

    re_path(r'^user/logout/$', views.HypoxicUserLogoutView.as_view(), name='user-logout'),

    # password reset
    re_path(r'^password/reset/$', views.HypoxicPasswordResetView.as_view(), name='password-reset-display'),
    re_path(r'^password/reset/confirm/$', views.HypoxicPasswordResetConfirmView.as_view(), name='password-reset'),
]
