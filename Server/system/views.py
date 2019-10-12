import time
from django.db.models import Max
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


# 存放当前检测结果
result = {}
get_in_result = {}
current_res_img = np.zeros((50, 25, 3), np.uint8)  # 初始化空白图片
current_username = ''
is_get_in_or_out = False  # 相当于进程控制

"""
检查用户合法性
post请求格式:
            username:用户名
            password:密码
返回:用户存在json格式"True",否则"False"
"""


@csrf_exempt
def check_user(request):
    global current_username
    username = str(request.POST.get('username'))
    password = str(request.POST.get('password'))
    user = models.User.objects.filter(name = username, password = password)
    # print(username, " ", password)
    res = {'status': 'False'}
    if user:
        res['status'] = 'True'  # 如果用户存在，True
        current_username = username
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


"""
处理一帧，返回检测结果
"""


@csrf_exempt
def handle(request):
    global result
    global current_res_img
    # 如果正在处理get_in 和get_out，则直接返回上一检测图片
    if is_get_in_or_out:
        nothing, buffer = cv2.imencode('.png', current_res_img)
        data = base64.b64encode(buffer)
        return HttpResponse(data, content_type = "image/png")  # 返回图片类型
    data = request.POST.get('image')
    img = base64_to_cv2(data)
    res = HyperLPR_PlateRecogntion(img)
    # initialize
    current_res_img = np.zeros((50, 25, 3), np.uint8)
    result['color'] = ''
    result['license_plate'] = ''
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


@csrf_exempt
def get_current_result(request):
    global result
    global current_res_img
    global get_in_result
    global is_get_in_or_out
    is_get_in_or_out = True
    state = str(request.POST.get('username'))  # 用username来保存是进入还是离开，懒得改了
    try:
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        result['time'] = current_time
        time_stamp = str(time.time())  # 转换为时间戳
        # 保存图片，注意路径
        cv2.imwrite(os.getcwd() + '\\system\\static\\images\\' + time_stamp + '.jpg', current_res_img)  # 以时间戳命名图片
        # print(os.getcwd() + '\\system\\static\\images\\' + time_stamp + '.jpg')
        result['image'] = time_stamp + '.jpg'
        result['price'] = 0.0
        if state == "False":
            result['price'] = calculate_price(result['time'])
        get_in_result = result
        return HttpResponse(json.dumps(result, ensure_ascii = False, indent = 4))
    except Exception as e:
        print(e, " error 2")
        return HttpResponse(json.dumps(result, ensure_ascii = False, indent = 4))


"""
用户进入和离开，记录保存数据库
"""


@csrf_exempt
def get_in_and_out(request):
    global get_in_result
    global result
    global is_get_in_or_out
    global current_res_img
    try:
        state = str(request.POST.get('username'))  # 用username来保存是进入还是离开，懒得改了
        new_history = models.History()
        new_history.name = current_username
        new_history.photograph = get_in_result['image']
        new_history.license_plate = get_in_result['license_plate']
        new_history.type = '大车' if get_in_result['color'] == '黄' else '小车'
        new_history.state = True if state == "False" else False
        new_history.price = get_in_result['price']
        new_history.time = get_in_result['time']
        if state == "False":
            new_history.price = calculate_price(get_in_result['time'])
        img = cv2.imread(os.getcwd() + '\\system\\static\\images\\' + get_in_result['image'])
        if len(img) < 100:
            is_get_in_or_out = False
            return HttpResponse(json.dumps({'state': 'failed'}, ensure_ascii = False, indent = 4))
        new_history.save()
        is_get_in_or_out = False
        return HttpResponse(
                json.dumps({'state': 'success', 'price': new_history.price}, ensure_ascii = False, indent = 4))
    except Exception as e:
        print(e, " error 1")
        is_get_in_or_out = False
        return HttpResponse(json.dumps({'state': 'failed'}, ensure_ascii = False, indent = 4))


"""
计算费用
"""


def calculate_price(get_out_time):
    get_in_histories = models.History.objects.filter(name = current_username)
    # 查询最新进入时间
    get_in_time = get_in_histories[0].time
    for i in get_in_histories:
        if i.time > get_in_time:
            get_in_time = i.time
    get_out_time = datetime.datetime.strptime(get_out_time, '%Y-%m-%d %H:%M:%S')
    get_in_time = get_in_time.replace(tzinfo = None)  # 解决时区问题，否则后面连加减都无法进行
    get_out_time = get_out_time.replace(tzinfo = None)
    get_in_time += datetime.timedelta(hours = 8)  # 不能直接hour加8
    # get_out_time += datetime.timedelta(hours = 8) #传进来的get_out_time不用加！！
    delta_time = get_out_time - get_in_time
    delta_time = delta_time.seconds  # 两个时间相差多少秒
    print(get_in_time, " ", get_out_time)
    print(delta_time, " *********************************************************")
    price = 0.0
    price_standard = models.PriceStandard.objects.all()[0]
    # 如果小于一小时，按一小时计
    get_in_time_hour = get_in_time.hour
    get_out_time_hour = get_out_time.hour
    if delta_time <= 3600:
        return price_standard.first_hour_price
    else:
        get_in_time_hour += 1
    # 如果停了超过一天，就先加上整数天的price
    if delta_time > 86400:
        days = int(delta_time / 86400)
        price += days * (price_standard.night_time_price * 12 + price_standard.day_time_price * 12)
        delta_time /= 86400
    # 计算每小时的费用
    while get_in_time_hour < get_out_time_hour:
        # 夜间价格
        if get_in_time_hour > 19 or get_in_time_hour < 7:
            price += price_standard.night_time_price
        else:
            price += price_standard.day_time_price
    return price


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