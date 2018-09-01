import random

from django.db import models
from django.db import IntegrityError

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
