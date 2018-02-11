import xadmin
from posts.models import Tag, Post


class TagAdmin(object):
    # 显示的字段
    list_display = ["name", "slug"]


class PostAdmin(object):
    # 显示的字段
    list_display = ["author", "title", "slug", "description", "is_active", "tags",
                    "created_on", "updated_on"]
    # 搜索字段


xadmin.site.register(Tag, TagAdmin)
xadmin.site.register(Post, PostAdmin)
