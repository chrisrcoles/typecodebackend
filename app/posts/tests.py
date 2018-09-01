import json

from django.test import Client
from django.test import TestCase
from django.utils import timezone
from .helpers import serialize_data, get_post_attrs, create_post

from .models import Post


class PostTestCase(TestCase):
    def setUp(self):
        self.POST1 = POST1 = {
            "title": "Post title",
            "slug": "post-title",
            "author": "John Doe",
            "body": "Some words go here",
            "published_date": timezone.now()

        }

        self.post1 = Post.objects.create(**POST1)
        self.CLIENT = Client(enforce_csrf_checks=False)


    # UnitTests
    def test_get_post_attrs(self):
        attrs = get_post_attrs(self.post1)

        self.assertEqual(self.post1.id, attrs["id"])
        self.assertEqual(self.post1.author, attrs["author"])
        self.assertEqual(self.post1.title, attrs["title"])
        self.assertEqual(self.post1.slug, attrs["slug"])
        self.assertEqual(self.post1.body, attrs["body"])
        self.assertEqual(self.post1.created_at,attrs["created_at"])
        self.assertEqual(self.post1.updated_at, attrs["updated_at"])
        self.assertEqual(self.post1.published_date, attrs["published_date"])


    def test_serialize_data(self):
        byte_string = b'{"message": "hello world"}'
        serialized_string = serialize_data(byte_string)
        self.assertEqual({"message": "hello world"}, serialized_string)


    def test_create_post(self):
        request_body = b'{ "title": "Post 2", "slug": "post-2", "author": "Willy Beem", "body": "Some words about post 2 go here" }'
        response = create_post(request_body)

        self.assertEqual(201, response.status_code)
        self.assertEqual({}, serialize_data(response.content))


    # Functional Tests for Endpoints
    def test_home(self):
        response = self.CLIENT.get('')
        data = serialize_data(response.content)
        self.assertEqual("Typecode API", data["message"])
        self.assertEqual(200, response.status_code)


    def test_get_all_posts_endpoint(self):
        response = self.CLIENT.get('/api/v1/posts/')
        data = serialize_data(response.content)
        self.assertEqual(2, data['_meta']['total_count'])
        self.assertEqual(self.post1.author, data['_meta']['objects'][1]['author'])
        self.assertEqual(self.post1.slug, data['_meta']['objects'][1]['slug'])
        self.assertEqual(self.post1.body, data['_meta']['objects'][1]['body'])
        self.assertEqual(200, response.status_code)


    def test_create_post_endpoint(self):
        data = {
            "title": "Building Rocket Ships From Here to There",
            "slug": "building-rocket-ships-from-here-to-there",
            "author": "Elon Musk",
            "body": "Some words about rocket ships here",
        }
        payload = json.dumps(data).encode('utf-8')
        response = self.CLIENT.post('/api/v1/posts/', data=payload, content_type='application/json')
        res = serialize_data(response.content)
        self.assertEqual({}, res)
        self.assertEqual(201, response.status_code)


    def test_get_post_by_slug_endpoint(self):
        slug = self.post1.slug
        response = self.CLIENT.get('/api/v1/posts/{}/'.format(slug))
        res = serialize_data(response.content)
        self.assertEqual(self.post1.author, res["author"])
        self.assertEqual(self.post1.body, res["body"])
        self.assertEqual(200, response.status_code)


    def test_update_post_by_slug_endpoint(self):
        slug = self.post1.slug
        update = { "author": "Jane Doe" }
        payload = json.dumps(update).encode('utf-8')
        response = self.CLIENT.put('/api/v1/posts/{}/'.format(slug), data=payload, content_type='application/json')
        res = serialize_data(response.content)
        self.assertEqual(self.post1.title, res["title"])
        self.assertEqual(update["author"], res["author"])
        self.assertEqual(200, response.status_code)


    def test_delete_post_by_slug_endpoint(self):
        slug = self.post1.slug
        response = self.CLIENT.delete('/api/v1/posts/{}/'.format(slug))
        res = serialize_data(response.content)
        self.assertEqual({}, res)
        self.assertEqual(200, response.status_code)
