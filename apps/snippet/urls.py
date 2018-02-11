from django.conf.urls import url, include
from django.views.static import serve
from rest_framework.urlpatterns import format_suffix_patterns

from snippet.views import snippet_list, snippet_detail, SnippetList, SnippetDetail,UserList,UserDetail

urlpatterns = [
    url(r'^$', snippet_list, name='index'),
    # snippet列表-fvb模式
    url(r'snippet/$', snippet_list, name='snippet_list'),
    # snippet详情-fvb模式
    url(r'snippet/(?P<pk>[0-9]+)/$', snippet_detail, name='snippet_detail'),
    # snippets列表-cvb模式
    url(r'^snippets/$', SnippetList.as_view()),
    # snippets详情-cvb模式
    url(r'^snippets/(?P<pk>[0-9]+)/$', SnippetDetail.as_view()),
    # users列表-cvb模式
    url(r'^users/$', UserList.as_view(), name='user_list'),
    # snippets详情-cvb模式
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view(), name='user_detail'),
]
# 设置后缀
urlpatterns = format_suffix_patterns(urlpatterns)