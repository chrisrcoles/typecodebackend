
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from posts.helpers import get_all_posts, create_post, get_update_or_delete_post
from posts.models import Post


def home(request):
    return JsonResponse({"message": "Typecode API"}, status=200)

# Create your views here.
@csrf_exempt
def get_or_create_posts(request):
    if request.method == 'GET':
        return get_all_posts()

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