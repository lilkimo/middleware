from .utils.request import requests, RequestArgs

from django.http import JsonResponse
urls = ['http://127.0.0.1:8001', 'http://127.0.0.1:8001', 'http://127.0.0.1:8002']

def handler(request, path):
    return JsonResponse(
        requests(
            urls,
            RequestArgs(
                request.method,
                path,
                request.headers,
                request.body,
                request.GET.dict()
            )
        ).json(),
        safe=False
    )
