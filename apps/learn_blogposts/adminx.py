import xadmin
from .models import Blogpost, Comment

# from .models import IndexAd,HotSearchWords


class BlogpostAdmin(object):
    list_display = ('title', 'slug', 'description', 'content', 'allow_comments', 'author', 'created', 'modified')
    readonly_fields = ('slug', 'created', 'modified', 'author')


class CommentAdmin(object):
    list_display = ('blogpost', 'content', 'author', 'created', 'modified')
    readonly_fields = ('created', 'modified', 'blogpost', 'author')


xadmin.site.register(Blogpost, BlogpostAdmin)
xadmin.site.register(Comment, CommentAdmin)





