from django.db import models
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization


# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)

    slug = models.CharField(max_length=200, unique=True)

    author = models.CharField(max_length=200)

    body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    published_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.title


class PostResource(ModelResource):
    class Meta:
        queryset = Post.objects.all()
        resource_name = 'posts'
        authorization = Authorization()
