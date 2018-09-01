# Create your views here.
from django.http import JsonResponse


def home(request):
    return JsonResponse({"message": "Typecode API"}, status=200)
