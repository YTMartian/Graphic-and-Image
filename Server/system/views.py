from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
import base64
import numpy as np


def index(request):
    return render(request, 'system/index.html')


def print_(request):
    return render(request, 'system/print.html')


@csrf_exempt
def handle(request):
    data = request.POST.get('image')
    img = base64_to_cv2(data)
    img = cv2.line(img, (0, 0), (len(img[0]), len(img)), (0, 0, 255), 5)
    img = cv2.line(img, (len(img[0]), 0), (0, len(img)), (0, 0, 255), 5)
    # cv2 image转base64
    nothing, buffer = cv2.imencode('.png', img)
    data = base64.b64encode(buffer)
    return HttpResponse(data, content_type = "image/png")  # 返回图片类型


# base64格式的字符串转换为opencv能处理的图片
def base64_to_cv2(uri):
    encoded_data = uri.split(',')[1]
    np_arr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img

# 对于第一帧有车牌的图像，识别之，并设置相关标记变量；
# 对于之后的图像，如果仍然有车牌，直接标注为上一帧图像的车牌号；
# 直到出现不含车牌的图像，重置相关标记变量
