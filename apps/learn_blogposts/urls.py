from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedSimpleRouter

from .views import BlogpostViewSet, CommentViewSet, NestedCommentViewSet


router = DefaultRouter()
router.register(r'blogposts', BlogpostViewSet)
router.register(r'comments', CommentViewSet)
# 用法，router 使用上一层级的router, r'blogposts'是上一级的前缀，lookup是上一级的model名字小写
blogposts_router = NestedSimpleRouter(router, r'blogposts', lookup='blogpost')
blogposts_router.register(r'comments', NestedCommentViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/', include(blogposts_router.urls)),
    # url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
]