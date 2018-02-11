from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    deploy_create_user = serializers.HyperlinkedRelatedField(many=True, view_name='api:deploypool-detail', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'deploy_create_user',)


class TokenSerializer(serializers.ModelSerializer):
    token = serializers.ReadOnlyField(source='create_user.username')

    class Meta:
        model = User
        fields = ('id', 'username', 'code', 'linenos', 'language', 'style')


class ServerSerializer(serializers.HyperlinkedModelSerializer):
    ip_subserver = serializers.HyperlinkedRelatedField(many=True, view_name='api:subserver-detail', read_only=True)
    # app_name = serializers.ReadOnlyField(source='app_name.name')

    class Meta:
        model = Server
        fields = ('id', 'server_env', 'name', 'server_sys', 'ip_subserver')


class SubserverSerializer(serializers.HyperlinkedModelSerializer):
    app_name = serializers.HyperlinkedRelatedField(view_name='api:app-detail', read_only=True)
    # server_ip = serializers.ReadOnlyField(source='server_ip.name')

    class Meta:
        model = SubServer
        fields = ('id', 'deploy_status', 'app_name', )


class SiteSerializer(serializers.HyperlinkedModelSerializer):
    app_name = serializers.HyperlinkedRelatedField(many=True, view_name='api:app-detail', read_only=True)

    class Meta:
        model = Site
        fields = ('id', 'name', 'app_name')


class SiteListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Site
        fields = ('id', 'name')


class DeployPoolSerializer(serializers.ModelSerializer):
    create_user = serializers.ReadOnlyField(source='create_user.username')
    site_name = serializers.ReadOnlyField(source='site_name.name')
    version_name = serializers.ReadOnlyField(source='version_name.name')
    app_name = serializers.ReadOnlyField(source='app_name.name')

    class Meta:
        model = DeployPool
        fields = ('id', 'name', 'site_name', 'version_name', 'app_name',
                  'order_no', 'deploy_status', 'deploy_progress', 'create_user', 'change_date' )


class AppSerializer(serializers.HyperlinkedModelSerializer):
    site_app = serializers.HyperlinkedRelatedField(many=True, view_name='api:site-detail', read_only=True)

    class Meta:
        model = SubServer
        fields = ('id', 'name', 'site_app',)


class VersionPoolSerializer(serializers.ModelSerializer):
    # 注意外键名称显示，nest field显示时的配置
    site_name = serializers.ReadOnlyField(source='site_name.name')
    dep_version = DeployPoolSerializer(many=True, required=False, read_only=True)
    create_user = serializers.ReadOnlyField(source='create_user.username')

    class Meta:
        model = VersionPool
        fields = ('id', 'name', 'site_name', 'is_order', 'version_progress',  'dep_version', 'create_user', 'add_date')