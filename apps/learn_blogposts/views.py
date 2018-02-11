"""
The API is where things get interesting. The access to the blogposts is exposed through a DRF ModelViewSet,
 which provides the usual actions:
list: GET /api/blogposts/      List all blogposts.
create: POST /api/blogposts/    Create a new blogpost.
retrieve: GET /api/blogposts/(?P<pk>[^/.]+)/    Show the details of a specific blogpost.
update: PUT /api/blogposts/(?P<pk>[^/.]+)/       Update all fields of a specific blogpost.
partial update: PATCH /api/blogposts/(?P<pk>[^/.]+)/     Update a field of a specific blogpost.
destroy: DELETE /api/blogposts/(?P<pk>[^/.]+)/ Delete a specific blogpost.

The rest of the comment actions are exposed through a top-level /comments endpoint. The reason for this is that
 I (and others believe) that resources should be accessible through a single URI.
list: GET /api/comments/    List all blogposts.
retrieve: GET /api/comments/(?P<pk>[^/.]+)/      Show the details of a specific comment.
update: PUT /api/comments/(?P<pk>[^/.]+)/       Update all fields of a specific comment.
partial update: PATCH /api/comments/(?P<pk>[^/.]+)/       Update a field of a specific comment.
destroy: DELETE /api/comments/(?P<pk>[^/.]+)/         Delete a specific comment.
整个项目的核心是如何实现嵌套资源访问，可以通过文章找到对应的评论
list: GET /api/blogposts/(?P<blogpost_pk>[^/.]+)/comments    List all the comments on a specific blogpost.
create: POST /api/blogposts/(?P<blogpost_pk>[^/.]+)/comments     Create a new comment on a specific blogpost.
"""
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.mixins import (
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin, CreateModelMixin
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import Blogpost, Comment
from .permissions import (
    IsAuthorOrReadOnly, CommentDeleteOrUpdatePermission, CommentsAllowed
)
from .serializers import BlogpostSerializer, CommentSerializer


class BlogpostViewSet(ModelViewSet):
    serializer_class = BlogpostSerializer
    queryset = Blogpost.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentViewSet(
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, ListModelMixin, GenericViewSet
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, CommentDeleteOrUpdatePermission)


class NestedCommentViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly, CommentsAllowed)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_blogpost(self, request, blogpost_pk=None):
        """
        Look for the referenced blogpost
        """
        # Check if the referenced blogpost exists
        blogpost = get_object_or_404(Blogpost.objects.all(), pk=blogpost_pk)

        # Check permissions
        self.check_object_permissions(self.request, blogpost)

        return blogpost

    def create(self, request, *args, **kwargs):
        self.get_blogpost(request, blogpost_pk=kwargs['blogpost_pk'])

        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            blogpost_id=self.kwargs['blogpost_pk']
        )

    def get_queryset(self):
        return Comment.objects.filter(blogpost=self.kwargs['blogpost_pk'])

    def list(self, request, *args, **kwargs):
        self.get_blogpost(request, blogpost_pk=kwargs['blogpost_pk'])

        return super().list(request, *args, **kwargs)
