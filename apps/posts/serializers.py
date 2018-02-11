from rest_framework.reverse import reverse

from rest_framework import serializers
from posts.models import Post, Tag


class TagSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tag
        fields = ('name', 'url')


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.Field(source='author.username')
    tags_details = TagSerializer(source='tags', read_only=True)
    api_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'title', 'description', 'created_on', 'author', 'tags',
                  'tags_details', 'url', 'api_url')
        read_only_fields = ('id', 'created_on')
        extra_kwargs = {
            'url': {'view_name':'posts', 'lookup_field':'pk'}
        }

    def get_api_url(self, obj):
        return "#/post/%s" % obj.id
