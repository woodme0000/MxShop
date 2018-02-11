import random, time
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication,BaseAuthentication

from utils.permissions import IsOwnerOrReadOnly
from .serializers import ShoppingCartSerializer, ShoppingCartDetailSerializer, OrderInfoSerializer
from .models import ShoppingCart, OrderGoods, OrderInfo

# Create your views here.


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
    list:
        获取购物车
    create:
        创建购物车
    update:
        更新购物车
    destroy：
        删除购物车
    retrieve:
        查找购物车
    """
    serializer_class = ShoppingCartSerializer

    # 增加用户是否登录的权限验证，用户未登录情况下，访问这个viewset，就会抛出一个401错误
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    # 添加用户认证机制，支持session认证和JSONWebToken认证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    lookup_field = 'goods_id'

    def get_serializer_class(self):
        if self.action == 'create':
            return ShoppingCartSerializer
        elif self.action == 'list':
            return ShoppingCartDetailSerializer
        else:
            return ShoppingCartSerializer

    # 为了保证只能看到自己的收藏，需要重载我们的get_queryset(self)
    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)


class OrderInfoViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin,
                       mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
    """
    list:
        获取个人订单列表
    create:
        新增一条订单
    delete:
        删除订单
    """
    serializer_class = OrderInfoSerializer

    # 增加用户是否登录的权限验证，用户未登录情况下，访问这个viewset，就会抛出一个401错误
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    # 添加用户认证机制，支持session认证和JSONWebToken认证
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return OrderInfo.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # 因为要生成一个order_sn，所以我们自己写实现
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)
        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()

            shop_cart.delete()
        return order
