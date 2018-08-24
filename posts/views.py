import json

from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from posts.helpers import get_post_attrs, serialize_data
from posts.models import Post


def home(request):
    return JsonResponse({"message": "Typecode API"}, status=200)

# Create your views here.
@csrf_exempt
def get_or_create_posts(request):
    if request.method == 'GET':
        return get_posts()

    elif request.method == 'POST':
        return create_post(request.body)


@csrf_exempt
def get_update_or_delete_post_by_id(request, post_id):
    try:
        post = Post.objects.get(pk=int(post_id))
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": "Post with ID `{}` does not exist.".format(post_id)}, status=404)

    return get_update_or_delete_post(request.method, request.body, post)


@csrf_exempt
def get_update_or_delete_post_by_slug(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except ObjectDoesNotExist as e:
        return JsonResponse({"message": "Post with slug `{}` does not exist.".format(slug)}, status=404)

    return get_update_or_delete_post(request.method, request.body, post)


# Helpers
def get_update_or_delete_post(method, request_body, post):
    data = get_post_attrs(post)
    if method == 'GET':
        return JsonResponse(data, safe=False, status=200)

    elif method == 'PUT':
        body = serialize_data(request_body)

        for val in body:
            setattr(post, val, body[val])

        post.save()
        return JsonResponse(get_post_attrs(post), safe=False, status=200)

    elif method == 'DELETE':
        post.delete()
        return JsonResponse({}, safe=False, status=200)


def create_post(request_body):
    body = serialize_data(request_body)
    Post.objects.create(**body)
    return JsonResponse({}, safe=False, status=201)


def get_posts():
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
