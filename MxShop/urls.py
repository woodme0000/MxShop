"""MxShop URL Configuration"""

from django.conf.urls import url, include
from django.views.static import serve

import xadmin
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token
from MxShop.settings import MEDIA_ROOT
# from goods.views_base import GoodsListView
from goods.views import GoodsListView, GoodsViewSet, CategoryViewSet, BannerViewSet,\
    IndexCategoryViewSet
from user_operation.views import UserFavViewSet, UserLeavingMessageViewSet, AddressViewSet
from users.views import SmsCodeViewSet, UserViewSet
from trade.views import ShoppingCartViewSet, OrderInfoViewSet
from musics.views import MusicViewSet

# =================================================================================
# Create a router and register our viewsets with it.
root_router = DefaultRouter()

# category的url
root_router.register(r'categorys', CategoryViewSet, base_name='categorys')
# 商品的url
root_router.register(r'goods', GoodsViewSet, base_name='goods')
# 用户收藏的url
root_router.register(r'userfavs', UserFavViewSet, base_name='userfavs')
# banner 的url
root_router.register(r'banners', BannerViewSet, base_name='banners')
# 首页商品系列数据 的url
root_router.register(r'indexcategorys', IndexCategoryViewSet, base_name='indexcategorys')
# code
root_router.register(r'code', SmsCodeViewSet, base_name='code')
# user注册
root_router.register(r'users', UserViewSet, base_name='users')
# 用户留言功能
root_router.register(r'messages', UserLeavingMessageViewSet, base_name='messages')
# 收货地址
root_router.register(r'address', AddressViewSet, base_name='address')
# 购物车
root_router.register(r'shopcarts', ShoppingCartViewSet, base_name='shopcarts')
# 订单
root_router.register(r'orders', OrderInfoViewSet, base_name='orders')





# ============================================= learn，使用as_view绑定http的行为和函数=#
goods_list = GoodsViewSet.as_view({
    'get': 'list',
})
# =================================================================================
from users.api_root import api_root
urlpatterns = [
    url(r'^', include(root_router.urls, namespace='goods')),
    # 管理后台url
    url(r'^xadmin/', xadmin.site.urls),
    # 图片访问url
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    # 商品列表页
    url(r'goods/$', goods_list, name='viewset_demo'),
    # drf 项目接口文档
    url(r'docs/', include_docs_urls(title='muxueshegnxian')),
    # drf 登录授权窗口
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # 这个是 rest framework jwt 认证的模式
    url(r'^login/', obtain_jwt_token),
    # snippet
    url(r'^api/', include('snippet.urls', namespace='snippet')),
    # user
    url(r'^api/', include('users.urls', namespace='user')),
    # musics ,相关的view_set都注册到那儿
    url(r'^api/', include('musics.urls', namespace='musics')),
    # posts ,
    url(r'^api/', include('posts.urls', namespace='posts')),
    # api_root
    url(r'^api-root/', api_root),
    # 验证DRF对嵌套post的支持
    # url(r'^blogpost/', include('learn_blogposts.urls', namespace='learn_blogposts'))
    # 验证drf对嵌套post支持
    #url(r'^postapi', include('api.urls',namespace='postapi')),
]
