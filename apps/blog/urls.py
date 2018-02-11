
from django.conf.urls import include, url
from django.contrib import admin

from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from blog.views import BlogpostViewSet, CommentViewSet, NestedCommentViewSet

from users.views import UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'blogposts', BlogpostViewSet)
router.register(r'comments', CommentViewSet)

blogposts_router = NestedSimpleRouter(router, r'blogposts', lookup='blogpost')
blogposts_router.register(r'comments', NestedCommentViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api/', include(blogposts_router.urls)),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]
