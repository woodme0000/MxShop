from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from django.http import Http404
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from posts.models import Post, Tag
from posts.serializers import PostSerializer, TagSerializer
from posts.permissions import IsOwnerOrReadOnly


class PostList(generics.ListCreateAPIView):
    """
    List all boards, or create a new board.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def pre_save(self, obj):
        obj.author = self.request.user


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a board instance.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class TagList(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        """
        This view should return a list of
            if q, all tags that contain q
            else, all tags
        """
        queryset = Tag.objects.all()
        query = self.request.query_params.get('q', None)
        if query is not None:
            queryset = queryset.filter(name__icontains=query)
        return queryset


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a tag instance.
    """
    quertset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)