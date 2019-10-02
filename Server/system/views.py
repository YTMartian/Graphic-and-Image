from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import base64


def index(request):
    return render(request, 'system/index.html')


def print_(request):
    return render(request, 'system/print.html')


@csrf_exempt
def handle(request):
    data = request.POST.get('image')
    image = base64.b64decode(str(data[22:]))  # base64格式的字符串转换为图片
    return HttpResponse(data)