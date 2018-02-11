from django.contrib.auth import get_user_model
from rest_framework import serializers
from snippet.models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

User = get_user_model()


class SnippetSerializer(serializers.Serializer):
    """
    字段数量一般是与model一一对应的，一般可以比model字段少，但不可以多，如果想增加需要另外进行处理！
    字段设置是为了验证前端通过get等方法传递过来的数据
    """
    # read_only 只读
    id = serializers.IntegerField(read_only=True)
    # required：必要， allow_blank:允许为空，
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    # style: 设置显示样式，控制如何显示可浏览的API
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data):
        """
        根据传入的数据创建一个实例
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        更新一个实例，若没有传值，就使用原来的数据
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance


class SnippetSerializer(serializers.ModelSerializer):
    # 只被用于序列化呈现，而不会被用于更新模型实例
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style','owner')
    # 默认实现了create()和 update()方法


# Serializers define the API representation.
class UserSerializer(serializers.ModelSerializer):

    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        # 定义了我们序列化的模型和显示的字段， url为网络接口
        # snippets为反向引用，不会被默认包含，所以需要添加显示字段
        fields = ('id', 'username', 'snippets')
