import time

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
import base64
import numpy as np
from hyperlpr import *
from PIL import Image, ImageDraw, ImageFont
from . import models
import datetime
import json


def index(request):
    return render(request, 'system/index.html')


def print_(request):
    return render(request, 'system/print.html')


"""
检查用户合法性
post请求格式:
            username:用户名
            password:密码
返回:用户存在json格式"True",否则"False"
"""


@csrf_exempt
def check_user(request):
    username = str(request.POST.get('username'))
    password = str(request.POST.get('password'))
    user = models.User.objects.filter(name = username, password = password)
    print(username, " ", password)
    res = {'status': 'False'}
    if user:
        res['status'] = 'True'  # 如果用户存在，True
    res = json.dumps(res, ensure_ascii = False, indent = 4)
    return HttpResponse(res)


"""
注册
post请求格式:
            username:用户名
            password:密码
返回:用户存在则注册失败,返回json格式"False",否则"True"
"""


@csrf_exempt
def register_user(request):
    username = str(request.POST.get('username'))
    password = str(request.POST.get('password'))
    user = models.User.objects.filter(name = username)
    res = {'status': 'False'}  # 用户存在
    if not user:
        res['status'] = 'True'  # 如果用户不存在，则True，并添加用户
        new_user = models.User()
        new_user.name = username
        new_user.password = password
        new_user.save()
    res = json.dumps(res, ensure_ascii = False, indent = 4)
    return HttpResponse(res)


"""
查询历史记录
post请求格式:
            username:用户名
            license_plate:车牌号
            start:开始日期
            end:结束日期
"""


@csrf_exempt
def get_history(request):
    username = str(request.POST.get('username'))
    license_plate = str(request.POST.get('license_plate'))
    start = str(request.POST.get('start'))
    end = str(request.POST.get('end'))
    histories = models.History.objects.all()
    res = []
    temp = {}
    for history in histories:
        # 看查询项是否非空及符合
        if username != '' and str(history.name) != username:
            continue
        if license_plate != '' and str(history.license_plate) != license_plate:
            continue
        if start != '' and str(history.time + datetime.timedelta(hours = 8))[:10] < start:
            continue
        if end != '' and str(history.time + datetime.timedelta(hours = 8))[:10] > end:
            continue
        temp['用户名'] = str(history.name)
        temp['车牌号'] = str(history.license_plate)
        temp['车型'] = str(history.type)
        temp['状态'] = '离开' if history.state else '进入'
        temp['时间'] = str(history.time + datetime.timedelta(hours = 8))[:19]
        temp['收费'] = str(history.price)
        temp['图片'] = str(history.photograph)
        res.append(temp.copy())
    res = json.dumps(res, ensure_ascii = False, indent = 4)
    return HttpResponse(res)


# 存放当前检测结果
result = {}
current_res_img = np.zeros((640, 480, 3), np.uint8)  # 初始化空白图片

"""
处理一帧，返回检测结果
"""


@csrf_exempt
def handle(request):
    global result
    global current_res_img
    data = request.POST.get('image')
    img = base64_to_cv2(data)
    res = HyperLPR_PlateRecogntion(img)
    if len(res) > 0:
        crop_img = img[res[0][2][1]:res[0][2][3], res[0][2][0]:res[0][2][2]]  # 裁剪车牌区域
        color = detect_color(crop_img)
        # 保存当前检测结果
        result['color'] = color
        result['license_plate'] = res[0][0]
        img = cv2.rectangle(img, (res[0][2][0], res[0][2][1]), (res[0][2][2], res[0][2][3]), (0, 0, 255), 3)
        height = res[0][2][3] - res[0][2][1]
        width = res[0][2][2] - res[0][2][0]
        img = cv2.rectangle(img, (res[0][2][0], res[0][2][1] - int(0.5 * height)),
                            (res[0][2][0] + int(0.6 * width), res[0][2][1]), (0, 0, 255), -1)
        img = add_chinese_text(img, res[0][0] + color, res[0][2][0] + 1, res[0][2][1] - int(0.5 * height) + 2,
                               int(0.35 * height))
        current_res_img = img
    
    # cv2 image转base64
    nothing, buffer = cv2.imencode('.png', img)
    data = base64.b64encode(buffer)
    return HttpResponse(data, content_type = "image/png")  # 返回图片类型


"""
用户请求当前检测结果
"""


def get_current_result(request):
    global result
    global current_res_img
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    result['time'] = current_time
    time_stamp = str(time.time())  # 转换为时间戳
    # 保存图片，注意路径
    cv2.imwrite(os.getcwd() + '\\system\\static\\images\\' + time_stamp + '.jpg', current_res_img)  # 以时间戳命名图片
    # print(os.getcwd() + '\\system\\static\\images\\' + time_stamp + '.jpg')
    result['image'] = time_stamp + '.jpg'
    return HttpResponse(json.dumps(result, ensure_ascii = False, indent = 4))


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
def add_chinese_text(img, text, x, y, thickness):
    # 图像从OpenCV格式转换成PIL格式
    img_PIL = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 字体位于：C:\Windows\Fonts
    font = ImageFont.truetype('simhei.ttf', thickness)
    draw = ImageDraw.Draw(img_PIL)
    draw.text((x, y), text, font = font, fill = (255, 255, 255))
    # 转换回OpenCV格式
    img = cv2.cvtColor(np.asarray(img_PIL), cv2.COLOR_RGB2BGR)
    return img


# 判断车牌颜色
def detect_color(img):
    # BGR转HSV
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # cv2.imshow("ff", img)
    # cv2.waitKey(0)
    # 蓝色车牌范围
    lower = np.array([100, 50, 50])
    upper = np.array([140, 255, 255])
    # 根据阈值构建掩模
    mask = cv2.inRange(img, lower, upper)
    # 计算权值，掩膜后图片蓝色区域保留，为非零值
    w = 0
    for i in mask:
        w += i / 255
    zero = 0
    for i in w:
        zero += 1 if i == 0 else 0
    return "黄" if zero > len(w) - zero else "蓝"