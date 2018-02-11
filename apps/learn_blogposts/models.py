import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel


class UUIDIdMixin(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class AuthorMixin(models.Model):
    class Meta:
        abstract = True

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, editable=False, verbose_name=_('所有人'),
        related_name='%(app_label)s_%(class)s_owner'
    )


class Blogpost(TimeStampedModel, TitleSlugDescriptionModel, models.Model):
    """
    TimeStampedModel: 包含一些创建时间 和修改时间
    TitleSlugDescriptionModel：包含title字段、slug字段、description字段
    
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, editable=False, verbose_name=_('所有人'),
        related_name='%(app_label)s_%(class)s_owner')

    content = models.TextField(_('正文'), blank=True, null=True)

    allow_comments = models.BooleanField(_('允许评论'), default=True)

    def __str__(self):
        return self.title


class Comment(UUIDIdMixin, TimeStampedModel, AuthorMixin):

    blogpost = models.ForeignKey(
        Blogpost, editable=False, verbose_name=_('blogpost'), related_name='comments'
    )
    content = models.TextField(_('content'), max_length=255, blank=False, null=False)
