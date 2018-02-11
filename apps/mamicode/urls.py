# -*- coding: utf-8 -*-
from rest_framework.routers import DefaultRouter

mami_router = DefaultRouter()
mami_router.register(r'subserver', api_views.SubserverViewSet, base_name="subserver")
mami_router.register(r'deploypool', api_views.DeployPoolViewSet, base_name="deploypool")
mami_router.register(r'versionpool', api_views.VersionPoolViewSet, base_name="versionpool")
mami_router.register(r'users', api_views.UserViewSet, base_name="users")
mami_router.register(r'server', api_views.ServerViewSet, base_name="server")
mami_router.register(r'site', api_views.SiteViewSet, base_name="site")
mami_router.register(r'app', api_views.AppViewSet, base_name="app")