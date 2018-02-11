# -*- coding: utf-8 -*-
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    允许owner编辑对象
    """

    def has_object_permission(self, request, view, obj):
        # obj 是从数据表里面取出来的user
        # SAFE_METHODS 是否是安全的方法,如果是安全方法，我们就不做权限验证
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Instance must have an attribute named `owner`. 对象必须有一个叫做"owner"字段，因为obj就是我们操作的对象
        # 例如UserFav对象.owner就是取
        # 这个数据库里面对象的owner字段
        return obj.user == request.user
