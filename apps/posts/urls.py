from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from posts.views import TagList, TagDetail, PostList, PostDetail

urlpatterns = [
    url(r'^posts/$', PostList.as_view(), name='post-list'),
    url(r'^posts/(?P<pk>[0-9]+)/$', PostDetail.as_view(), name='post-detail'),
    url(r'^tags/$', TagList.as_view(), name='tag-list'),
    url(r'^tags/(?P<pk>[0-9]+)/$', TagDetail.as_view(), name='tag-detail'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
