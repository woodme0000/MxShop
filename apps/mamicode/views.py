from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets


@csrf_exempt
def gettoken():
    pass


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
    paginate_by = 10

    def get_queryset(self):
        queryset = self.queryset.filter(username='kevin')
        return queryset


class SiteViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = (permissions.AllowAny,)
    paginate_by = 10


class SiteListAPI(generics.ListAPIView):
    """
    This ListAPIView automatically provides `list` actions.
    """
    queryset = Site.objects.all()
    serializer_class = SiteListSerializer
    paginate_by = 1000


class AppViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = (permissions.AllowAny,)
    paginate_by = 10


class ServerViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    paginate_by = 10


class SubserverViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = SubServer.objects.all()
    serializer_class = SubserverSerializer
    permission_classes = (permissions.AllowAny,)
    paginate_by = 10

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DeployPoolViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    serializer_class = DeployPoolSerializer
    authentication_classes = (TokenAuthentication,)
    paginate_by = 1000

    def get_queryset(self):
        filter_dict = dict()

        if self.request.query_params.get('site_name'):
            filter_dict['site_name__name'] = self.request.query_params.get('site_name')
        if self.request.query_params.get('order_no'):
            filter_dict['order_no'] = self.request.query_params.get('order_no')
        if self.request.query_params.get('version_name'):
            if self.request.query_params.get('version_name') == "null":
                filter_dict['version_name__isnull'] = True
            else:
                filter_dict['version_name__name'] = self.request.query_params.get('version_name')
        # 以下过滤发布单的环境及时间(30天)
        # filter_dict['deploy_progress'] = u"待发布"
        filter_dict['deploy_status__in'] = ["UAT", "PRD", "SIM", "DRP", "BUILD", "FAT", "DEV"]
        current_date = timezone.now()
        filter_dict['change_date__gt'] = current_date - timedelta(days=3000)

        return DeployPool.objects.filter(**filter_dict)

    def update(self, request, *args, **kwargs):
        name = request.data['name']
        order_no = request.data['order_no']
        version_name = request.data['version_name']

        try:
            if version_name:
                version_item = VersionPool.objects.get(name=version_name)
                DeployPool.objects.filter(name=name).update(order_no=order_no, version_name=version_item)
            else:
                DeployPool.objects.filter(name=name).update(order_no=order_no, version_name=None)
            response_data = {
                'result': 'success',
                'name': name,
                'create_user': request.user.username,
                'message': '更新发布单成功！'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except:
            response_data = {
                'result': 'failed',
                'message': '更新发布单失败！'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class VersionPoolViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    Additionally we also provide an extra `highlight` action.
    """
    queryset = VersionPool.objects.all()
    serializer_class = VersionPoolSerializer
    authentication_classes = (TokenAuthentication,)
    paginate_by = 100

    def get_queryset(self):
        queryset = self.queryset
        return queryset

    # 如有需要，自定义update和create方法，以实现外键方面的关联
    def create(self, request, *args, **kwargs):
        name = request.data['name']
        site_name = request.data['site_name']
        validated_data = dict()
        validated_data['name'] = site_name + "-" + name
        try:
            validated_data['site_name'] = Site.objects.get(name=site_name)
        except:
            response_data = {
                'result': 'failed',
                'name': site_name + "-" + name,
                'create_user': request.user.username,
                'message': '项目名不存在！'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        validated_data['create_user'] = request.user
        try:
            VersionPool.objects.create(**validated_data)
            response_data = {
                'result': 'success',
                'name': site_name + "-" + name,
                'create_user': request.user.username,
                'message': '创建版本单成功！'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except:
            response_data = {
                'result': 'failed',
                'name': site_name + "-" + name,
                'create_user': request.user.username,
                'message': '已存在相同版本单'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):

        if request.data["isOrder"] == "false":
            is_order = False
        else:
            is_order = True

        print request.data, "%%%%%%%%%%%%%%%%%%%%%%%%%"

        VersionPool.objects.filter(id=kwargs["pk"]).update(is_order=is_order)

        try:
            response_data = {
                'result': 'success',
                'create_user':request.user.username,
                'message':'更新版本单成功!'
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except:
            response_data = {
                'result': 'failed',
                'message': '更新版本单失败！'
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)