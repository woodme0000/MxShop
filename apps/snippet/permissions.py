from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    设置权限只允许创建者编辑,不是创建者可以浏览
    """
    def has_object_permission(self, request, view, obj):
        # 为不同的请求设置权限，GET, HEAD or OPTIONS 为安全请求
        if request.method in permissions.SAFE_METHODS:
            return True
        # 写权限只有代码拥有者有，判断拥有者和请求者是否是同一个用户
        return obj.owner == request.user