from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from django.contrib.auth import get_user_model
User = get_user_model()


class Tag(models.Model):
    slug = models.SlugField(max_length=100, verbose_name=_('slug'), blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return "%s" % self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)


class Post(models.Model):
    """
    An item created by a user.
    """
    author = models.ForeignKey(User, related_name='posts', verbose_name='作者')
    title = models.CharField(u'标题', max_length=100)
    slug = models.SlugField()
    description = models.TextField(u'描述', blank=True, help_text=(
        "If omitted, the description will be the post's title."))
    is_active = models.BooleanField(u'状态', default=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='posts', verbose_name='标签')
    created_on = models.DateTimeField(u'添加时间', auto_now_add=True)
    updated_on = models.DateTimeField(u'更新时间', auto_now=True)

    def save(self, *args, **kwargs):
        self.do_unique_slug()
        if not self.description:
            self.description = self.title
        super(Post, self).save(*args, **kwargs)

    def do_unique_slug(self):
        """
        Ensures that the slug is always unique for this post
        """
        if not self.id:
            # make sure we have a slug first
            if not len(self.slug.strip()):
                self.slug = slugify(self.title)

            self.slug = self.get_unique_slug(self.slug)
            return True

        return False

    def get_unique_slug(self, slug):
        """
        Iterates until a unique slug is found
        """
        orig_slug = slug
        counter = 1

        while True:
            posts = Post.objects.filter(slug=slug)
            if not posts.exists():
                return slug

            slug = '%s-%s' % (orig_slug, counter)
            counter += 1

    def __str__(self):
        return self.title

