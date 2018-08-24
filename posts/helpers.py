import json

from django.core import serializers
from django.http import JsonResponse

from posts.models import Post


def get_post_attrs(post):
    return {
        "id": post.id,
        "author": post.author,
        "title": post.title,
        "slug": post.slug,
        "body": post.body,
        "created_at": post.created_at,
        "updated_at": post.updated_at,
        "published_date": post.published_date,
    }


def serialize_data(body):
    return json.loads(str(body, 'utf-8'))


def create_post(request_body):
    body = serialize_data(request_body)
    Post.objects.create(**body)
    return JsonResponse({}, safe=False, status=201)


def get_all_posts():
    posts = Post.objects.all()

    def serialize_post(post):
        post["fields"]["id"] = post["pk"]
        return post["fields"]

    return JsonResponse({
        "_meta": {
            "total_count": posts.count(),
            "objects": list(map(serialize_post, json.loads(serializers.serialize('json', posts))))
        }
    }, safe=False, status=200)


def get_update_or_delete_post(method, request_body, post):
    if method == 'GET':
        return get_post(post)

    elif method == 'PUT':
        return update_post(request_body, post)

    elif method == 'DELETE':
        return delete_post(post)


def get_post(post):
    data = get_post_attrs(post)
    return JsonResponse(data, safe=False, status=200)


def update_post(request_body, post):
    body = serialize_data(request_body)

    for val in body:
        setattr(post, val, body[val])

    post.save()
    return JsonResponse(get_post_attrs(post), safe=False, status=200)


def delete_post(post):
    post.delete()
    return JsonResponse({}, safe=False, status=200)