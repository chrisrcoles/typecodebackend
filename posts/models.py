import random
import uuid

from django.db import models
from django.conf.urls import url
from django.db import IntegrityError

from tastypie.resources import ModelResource
from tastypie.authorization import Authorization


# Create your models here.
class Post(models.Model):

    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=200, unique=True)

    slug = models.CharField(max_length=200, unique=True)

    author = models.CharField(max_length=200)

    body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    published_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        try:
            super(Post, self).save(*args, **kwargs)
        except IntegrityError as e:
            if 'unique constraint' and 'posts_post_title_key' in e.args[0]:
                rand = random.sample(range(1, 9), 5)
                string_rand = ''.join(map(str, rand))
                self.slug = self.slug + '-' + string_rand
                self.title = self.title + '-' + string_rand
                super(Post, self).save(*args, **kwargs)

class PostResource(ModelResource):
    class Meta:
        queryset = Post.objects.all()
        resource_name = 'posts'
        authorization = Authorization()
        detail_uri_name = 'id'

    def prepend_urls(self):
        return [
            url(r"^(?P<posts>%s)/(?P<id>[\w\d_.-]+)/$" % self._meta.resource_name,
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]
