from rest_framework import serializers
from .models import Blogpost, Comment


class BlogpostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blogpost
        fields = ('id', 'title', 'description', 'content', 'allow_comments',
                  'slug', 'owner', 'created', 'modified')
        read_only_fields = ('id', 'slug', 'owner', 'created', 'modified')


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ('url', 'content', 'owner', 'created', 'modified', 'blogpost')
        read_only_fields = ('url', 'owner', 'created', 'modified', 'blogpost')
