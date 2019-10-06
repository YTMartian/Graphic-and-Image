from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
import base64
import numpy as np
from hyperlpr import *
from PIL import Image, ImageDraw, ImageFont


def index(request):
    return render(request, 'system/index.html')


def print_(request):
    return render(request, 'system/print.html')


@csrf_exempt
def handle(request):
    data = request.POST.get('image')
    img = base64_to_cv2(data)
    # img = cv2.line(img, (0, 0), (len(img[0]), len(img)), (0, 0, 255), 5)
    # img = cv2.line(img, (len(img[0]), 0), (0, len(img)), (0, 0, 255), 5)
    res = HyperLPR_PlateRecogntion(img)
    if len(res) > 0:
        print(res)
        img = cv2.rectangle(img, (res[0][2][0], res[0][2][1]), (res[0][2][2], res[0][2][3]), (0, 0, 255), 3)
        height = res[0][2][3] - res[0][2][1]
        width = res[0][2][2] - res[0][2][0]
        img = cv2.rectangle(img, (res[0][2][0], res[0][2][1] - int(0.5 * height)),
                            (res[0][2][0] + int(0.5 * width), res[0][2][1]), (0, 0, 255), -1)
        img = addChineseText(img, res[0][0], res[0][2][0] + 1, res[0][2][1] - int(0.5 * height) + 2, int(0.35 * height))
    # cv2 image转base64
    nothing, buffer = cv2.imencode('.png', img)
    data = base64.b64encode(buffer)
    return HttpResponse(data, content_type = "image/png")  # 返回图片类型


# base64格式的字符串转换为opencv能处理的图片
def base64_to_cv2(uri):
    try:
        encoded_data = uri.split(',')[1]
        np_arr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        return img
    except:
        return ''


# 在图片中显示中文
def addChineseText(img, text, x, y, thickness):
    # 图像从OpenCV格式转换成PIL格式
    img_PIL = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 字体位于：C:\Windows\Fonts
    font = ImageFont.truetype('STXIHEI.TTF', thickness)
    draw = ImageDraw.Draw(img_PIL)
    draw.text((x, y), text, font = font, fill = (255, 255, 255))
    # 转换回OpenCV格式
    img = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)
    return img