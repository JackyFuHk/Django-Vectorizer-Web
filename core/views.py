import random
import string
import json
import urllib
import stripe
import logging
logger = logging.getLogger(__name__)
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from django.shortcuts import render, redirect  
from django.contrib.auth import authenticate, login, logout  
from django.contrib.auth.decorators import login_required  
from django.shortcuts import render, redirect  
from django.contrib.auth.forms import UserCreationForm  
from django.contrib import messages 
from django.contrib.staticfiles.storage import staticfiles_storage  
from .models import CustomAuthenticationForm,UserProfile,ActivateCode
import xml.etree.ElementTree as ET

from django.contrib.auth import authenticate  
from django.views.decorators.csrf import csrf_exempt
import re
import requests
from algorithm.pngtosvg import potracemyown
from django.shortcuts import render, redirect
from .email_send import send_verification_email, generate_verification_link
from .aliyun_sms import SMS
from django.shortcuts import render, redirect  
from django.contrib.auth.models import User  
from django.contrib.auth.forms import UserCreationForm  
from django.core.mail import send_mail  
from django.utils.crypto import get_random_string  
from django.conf import settings  
from django.http import HttpResponse  
from django.urls import reverse  
from django.contrib.sites.shortcuts import get_current_site  
import hashlib  
import uuid  
from .models import ImageHistory
from django.views.generic import TemplateView
from django.core.serializers.json import DjangoJSONEncoder
# 登录界面
def login_view(request):  
    if request.method == 'POST':  
        form = CustomAuthenticationForm(request, data=request.POST)  
        if form.is_valid():  
            username = form.cleaned_data.get('username')  
            password = form.cleaned_data.get('password')  
            user = authenticate(request, username=username, password=password)
    
            if user is not None:  
                login(request, user)  
                return redirect('/')  
    else:  
        form = CustomAuthenticationForm()  
    return render(request, 'login.html', {'form': form})  

def api_view(request):
    return render(request, 'api.html')


def reset_view(request):
    return render(request, 'reset.html') 

def reset(request):
    if request.method == 'POST':  
        data = json.loads(request.body)  
        email = data.get('email')
        password2 = data.get('password')
        certification_code = data.get('code')

        if certification_code != request.session['certification_code']:
            return JsonResponse({'code':'400','message': 'certification code is incorrect'})
 
        
        try:
            user = User.objects.get(username=email)
        except:
            return JsonResponse({'code':'400','message': 'your account is not exist.'})
        
        user.set_password(password2)
        user.save()
        
        return JsonResponse({'code':'200','status': 'success', 'message': '账户已创建'})  

@login_required  
def home_view(request):  
    user_info = {  
        'username': request.user.username,  
        'id': request.user.id,  
    } 
    
    return render(request, 'home.html',{'user': user_info})  
  
def logout_view(request):  
    logout(request)  
    return redirect('/')

@login_required
def account_view(request):
    user_info =  request.user

    email = request.user.email
    user = User.objects.get(email=email)
    user_profile = user.userprofile  
    endtime = user_profile.subscriptionEnd
    is_subscription = user_profile.is_subscription
    return render(request, 'account.html',{'user': user_info,'user_profile':user_profile})  

def generate_unique_username(email):  
    # 生成一个基于电子邮件和UUID的唯一用户名  
    base_username = email.split('@')[0]  # 取电子邮件地址中的本地部分  
    unique_suffix = uuid.uuid4().hex[:8]  # 取UUID的前8个字符作为唯一后缀  
    username = f"{base_username}_{unique_suffix}"  
      
    # 检查生成的用户名是否已存在，如果存在则递归调用直到找到唯一的用户名  
    if User.objects.filter(username=username).exists():  
        return generate_unique_username(email)  
    
    return username
def register_view(request):  
    form = UserCreationForm()  
    return render(request, 'register.html', {'form': form}) 

def register(request):  
    if request.method == 'POST':  
        data = json.loads(request.body)  
        email = data.get('email')
        password2 = data.get('password')
        certification_code = data.get('code')
        if certification_code != request.session['certification_code']:
            return HttpResponse('certification code is not correct.')  
        backend = 'django.contrib.auth.backends.ModelBackend'
        # backend = 'allauth.account.auth_backends.AuthenticationBackend'
        
        user = User.objects.create_user(username=email, email=email, password=password2)
        user_profile = UserProfile.objects.create(user=user, name=user.username)
        user.save()
        user.backend = backend  # 设置用户实例的后端属性
        today = datetime.now().date()
        # three_days_later_date = today + relativedelta(days=3)
        user_profile = user.userprofile  
        user_profile.is_subscription = False
        user_profile.subscriptionEnd = today
        user_profile.save()  # 别忘了保存更改
        login(request, user,backend=backend)  # 登录用户，传入backend参数
        return JsonResponse({'code':'200','status': 'success', 'message': '账户已创建'})  

def generate_verification_code(length=6):  
    """生成一个随机的验证码"""  
    return ''.join(random.choices(string.digits, k=length))  
   
# def register_send_certification(request):
  
#     if request.method == 'POST': 
#         data = json.loads(request.body)  
#         email = data.get('email')  
#         if email:  
#             # 生成验证码  
#             verification_code = generate_verification_code(length=4)  
#             request.session['certification_code'] = verification_code
#             # SMS.main(phone_number=email,code2=verification_code)  
            
#             return JsonResponse({'code':'200','status': 'success', 'message': '验证码已发送'})  
      
#     return JsonResponse({'code':'400','status': 'error', 'message': '无效的请求'}, status=400)  
# def sendsms(request):
#     # 获取所有用户
#     users = User.objects.all()
    
#     # 提取所有用户名
#     usernames = [user.username for user in users]
    
#     return render(request, 'blog/account.html', {'usernames': usernames})


def register_send_certification(request):
  
    if request.method == 'POST': 
        data = json.loads(request.body)  
        email = data.get('email')  
        if email:  
            # 生成验证码  
            verification_code = generate_verification_code(length=6)  
            request.session['certification_code'] = verification_code
            subject = 'VectorizerCN - Validation Code'  
            message = f'欢迎使用VectorizerCN矢量化工具网站. \n您的验证码为: {verification_code}'  
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)  
            
            return JsonResponse({'code':'200','status': 'success', 'message': '验证码已发送'})  
      
    return JsonResponse({'code':'400','status': 'error', 'message': '无效的请求'}, status=400)  

import pytz
@csrf_exempt
def is_subscription(request):
    if not request.user.is_authenticated:
        return JsonResponse({'is_auth': False})
    else:
        return JsonResponse({'is_auth': True})
    email = request.user.email
    user = User.objects.get(email=email)
    user_profile = user.userprofile  
    endtime = user_profile.subscriptionEnd
    is_subscription = user_profile.is_subscription
    utc_tz = pytz.utc
  
    now_utc = datetime.now(utc_tz)
   
    if now_utc <= endtime:
        return JsonResponse({'is_auth':True})
    else:
        return JsonResponse({'is_auth':False})

def verify_view(request, token):  
    try:  
        user = User.objects.get(username__iexact=token[:30])  # 假设token的前30个字符是username的哈希值  
        if hashlib.sha256((user.username + str(user.date_joined)).encode()).hexdigest() == token:  
            user.is_active = True  
            user.save()  
            return HttpResponse('Your account has been activated! You can now log in.')  
        else:  
            return HttpResponse('Invalid token')  
    except User.DoesNotExist:  
        return HttpResponse('Invalid token')
    


from django.shortcuts import render
from django.conf import settings





############################################################################
from django.http import JsonResponse
from PIL import Image
import cv2
import numpy as np
import base64

import os
import uuid
from datetime import timedelta, datetime 
import time
from django.utils.safestring import mark_safe 
from .forms import ContactForm  
from .models import Contact ,Post ,ConverterTools,ColorOptions,FullFeature,FAQs
def encodebase64(new_logo):
    data = cv2.imencode('.png', new_logo)[1]
    image_bytes = data.tobytes()
    img_data = base64.b64encode(image_bytes).decode('utf8')
    result = "data:image/png;base64," + str(img_data)
    return result


@csrf_exempt
def pngtosvg(request):  
    if request.method == 'POST':
        data = json.loads(request.body)  
        png_url = data.get('imgsrc')  
        index = data.get('index')
        name = data.get('name')

        svg_content= potracemyown.bitmap_to_bezier(png_url)

        response_data = {  
            'status': 'success',  
            # 'svg_content': svg_content,  # 如果你要返回 SVG 内容  
            'index':index,
            'name':name
        }  
        request.session[name] = svg_content
        
        # 写到 数据库里。用户名，工具url，原图url，转换后的svg图的字符串，是否已下载，时间。
        ImageHistory.objects.create(user_name=request.user.username,tool="png2svg", initial_img=png_url,svg_content=svg_content)
  
        return JsonResponse(response_data)
    
@csrf_exempt
def download_svg(request):
    if request.method == 'POST':
        data = json.loads(request.body)  
        png_url = data.get('imgsrc')  
        index = data.get('index')
        name = data.get('name')
        my_variable = request.session.get(name)
        response_data = {
            "data":my_variable
        }
        print(png_url)
        imagehistory = ImageHistory.objects.filter(user_name=request.user.username,is_download=False,tool="png2svg",initial_img=png_url)
        return JsonResponse(response_data)

@csrf_exempt
def getActivateCode(request):
    code = ActivateCode.objects.only('code').order_by('-created_at').first()
    return JsonResponse({"code":str(code)})


def home_download_svg(request):
    data = json.loads(request.body)  
    png_url = data.get('imgsrc')  
    index = data.get('index')
    name = data.get('name')
    my_variable = request.session.get(name)
    response_data = {
        "data":my_variable
    }


    media_root = settings.MEDIA_ROOT  
    cutoff_time = datetime.now() - timedelta(days=7)  
    cutoff_timestamp = cutoff_time.timestamp()  
    
    for root, dirs, files in os.walk(media_root):  
        for file in files:  
            if file.endswith('svg') or file.endswith('png'):
                file_path = os.path.join(root, file)  
                try:  
                    file_creation_time = os.path.getctime(file_path)  
                    if file_creation_time < cutoff_timestamp:  
                        os.remove(file_path)
                except:
                    pass
    # ImageHistory.objects.filter(user_name=request.user.username,is_download=False,tool="png2svg",initial_img=png_url).update(is_download = True)
    return JsonResponse(response_data)

def author_view(request):
    return render(request,  "author.html")

def about_us(request):
    return render(request,  "about_us.html")

def contact_view(request):  
    if request.method == 'POST':  
        form = ContactForm(request.POST)  
        if form.is_valid():  
            form.save()  
            return redirect('/support/')  
    else:  
        form = ContactForm()  
    return render(request, 'support.html', {'form': form})  
  
def contact_success_view(request):  
    return render(request,  "support.html")

  
def post_list(request):  
    posts = Post.objects.all().order_by('created_at')  
    return render(request, 'blog/post_list.html', {'posts': posts})  
  
def post_detail(request, slug):  
    post = get_object_or_404(Post, slug=slug)  
    posts = Post.objects.all().exclude(slug=slug)[:3]

    post.view_count += 1  
    post.save()  
    return render(request, 'blog/post_detail.html', {'post': post,'posts': posts})

def policy_term(request):
    return render(request,  "terms_of_service.html")

def policy_privacy(request):
    return render(request,  "privacy.html")

def custom_404_view(request, exception=None):  
    return render(request, '404.html', status=404)


def homeView(request):
    return render(request, "home.html",{'designnum':78})

def pngtosvg_view(request):
    if request.user.is_authenticated:
        imagehistory = ImageHistory.objects.filter(user_name=request.user.username,is_download=False,tool="png2svg")

        myall = list()
        

        index = 0
        for image in imagehistory:
            myimagehistory = {}
            request.session[image.initial_img] = image.svg_content
            myimagehistory['imgsrc'] = image.initial_img
            myimagehistory['imgname'] = image.initial_img
            myimagehistory['index'] = index 
            myall.append(myimagehistory)
            index +=1

        return render(request,'pngtosvg.html',{"imagehistory":imagehistory,"imagehistory_json":json.dumps(myall)})
    else:
        return render(request,'pngtosvg.html')
    


@csrf_exempt
def upload_image(request):
    if request.method == 'POST':  
        # 获取文件数据  
        if 'file' in request.FILES:  
            uploaded_file = request.FILES['file']  
        
            image = Image.open(uploaded_file).convert('RGBA')
            
            png_addr = os.path.join(settings.MEDIA_ROOT, "PNGTOSVG_{}_{}.png".format(datetime.now().strftime("%Y%m%d-%H%M%S"),uuid.uuid4()))  
            image.save(png_addr)
            
            svg_url = settings.MEDIA_URL + os.path.relpath(png_addr, settings.MEDIA_ROOT)  
            
            if 'http' not in svg_url:
                png_url = settings.DOMAIN_NAME + svg_url
            else:
                png_url = svg_url
   
        else:  
            uploaded_file = None  
        
        
        # 构建响应消息  
        response_data = {  
            'message': 'Image clicked! This is the response from the server.',  
            'user_png':png_url,
            'name':uploaded_file.name
        }  
  
        # 返回 JSON 响应  
        return JsonResponse(response_data)  
    else:  
        # 如果不是 POST 请求，返回错误消息或重定向到表单页面  
        return JsonResponse({'message': 'Invalid request method. Only POST requests are allowed.'}, status=400)

from .wechat_pay import WechatPayAPI
import qrcode
import hashlib
import requests
import json
@csrf_exempt
def make_order(request):
    # data = json.loads(request.body)
    # print(request.body)
    # order_id = data.get("order_id", 0)

    total_price = 0.01   # 订单总价
    order_name = 'test'   # 订单名字
    order_detail = 'test'   # 订单描述
    order_id = 20200411234567    # 自定义的订单号
    data_dict = wxpay(order_id, order_name, order_detail, total_price)   # 调用统一支付接口
    # 如果请求成功
    if data_dict.get('return_code') == 'SUCCESS':
        # 业务处理
        # 二维码名字
        qrcode_name = str(order_id) + '.png'
        # 创建二维码
        img = qrcode.make(data_dict.get('code_url'))
        img_url = os.path.join(settings.MEDIA_ROOT, qrcode_name)
        img.save(img_url)
        s = {
            "code": 1000,
            "msg": "获取成功",
            "data": img_url     # 访问路径
        }
        s = json.dumps(s, ensure_ascii=False)
        return HttpResponse(s)
    s = {
                "code": 1001,
                "msg": "获取失败"+str(data_dict),
                "data": ""
            }
    s = json.dumps(s, ensure_ascii=False)
    return HttpResponse(s)

def wx_result_n(request):
    data_dict = trans_xml_to_dict(request.body)  # 回调数据转字典
    print('支付回调结果', data_dict)
    sign = data_dict.pop('sign')  # 取出签名
    back_sign = get_sign(data_dict, settings.WECHAT_PAY_API_KEY)  # 计算签名
    # 验证签名是否与回调签名相同
    if sign == back_sign and data_dict['return_code'] == 'SUCCESS':
        order_no = data_dict['out_trade_no']
        # 处理支付成功逻辑，根据订单号修改后台数据库状态
        # 返回接收结果给微信，否则微信会每隔8分钟发送post请求
        return HttpResponse(trans_dict_to_xml({'return_code': 'SUCCESS', 'return_msg': 'OK'}))
    return HttpResponse(trans_dict_to_xml({'return_code': 'FAIL', 'return_msg': 'SIGNERROR'}))

def random_str(randomlength=32):
    """
    生成随机字符串
    :param randomlength: 字符串长度
    :return:
    """
    strs = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    import random
    for i in range(randomlength):
        strs += chars[random.randint(0, length)]
    print(strs)
    return strs


# 请求统一支付接口
def wxpay(order_id, order_name, order_price_detail, order_total_price):
    nonce_str = random_str()  # 拼接出随机的字符串即可，我这里是用  时间+随机数字+5个随机字母
    total_fee = int(float(order_total_price) * 100)    # 付款金额，单位是分，必须是整数
    print("total_fee",total_fee)    
    params = {
        'appid': settings.WECHAT_PAY_APP_ID,  # APPID
        'mch_id': settings.WECHAT_PAY_MCH_ID,  # 商户号
        'nonce_str': nonce_str,  # 随机字符串
        'out_trade_no': order_id,  # 订单编号，可自定义
        'total_fee': total_fee,  # 订单总   金额
        'spbill_create_ip': settings.CREATE_IP,  # 自己服务器的IP地址
        'notify_url': settings.WECHAT_PAY_NOTIFY_URL,  # 回调地址，微信支付成功后会回调这个url，告知商户支付结果
        'body': "test",  # 商品描述
        # 'detail': order_price_detail,  # 商品描述
        'trade_type': 'NATIVE',  # 扫码支付类型
    }

    sign = get_sign(params, settings.WECHAT_PAY_API_KEY)  # 获取签名
    params['sign'] = sign  # 添加签名到参数字典
    # params['product_id'] = '1234567890'
    xml = trans_dict_to_xml(params)  # 转换字典为XML
    print("xml",xml)
    response = requests.request('post', settings.UFDODER_URL, data=xml.encode())  # 以POST方式向微信公众平台服务器发起请求
    data_dict = trans_xml_to_dict(response.content)  # 将请求返回的数据转为字典
    print("data_dict",data_dict)
    return data_dict




def get_sign(data_dict, key):
    
    # 过滤掉 sign 字段和空值字段
    filtered_data = {k: v for k, v in data_dict.items() if k != "sign" and v not in [None, ""]}

    # 排序 + 拼接
    params_list = sorted(filtered_data.items(), key=lambda e: e[0])
    params_str = "&".join(f"{k}={v}" for k, v in params_list) + f"&key={key}"
   
    # MD5加密
    md5 = hashlib.md5()
    md5.update(params_str.encode('utf-8'))
    sign = md5.hexdigest().upper()
    print("签名前字符串:", params_str)
    print("签名结果:", sign)
    return sign

def recharge(request):
    return render(request, "recharge.html")  
def trans_dict_to_xml(data_dict):
    """
    定义字典转XML的函数
    :param data_dict:
    :return:
    """
    data_xml = []
    for k in sorted(data_dict.keys()):  # 遍历字典排序后的key
        v = data_dict.get(k)  # 取出字典中key对应的value
        if k == 'detail' and not v.startswith('<![CDATA['):  # 添加XML标记
            v = '<![CDATA[{}]]>'.format(v)
        data_xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
    return '<xml>{}</xml>'.format(''.join(data_xml))  # 返回XML


def trans_xml_to_dict(data_xml):
    """
    定义XML转字典的函数
    :param data_xml:
    :return:
    """
    data_dict = {}
    try:
        import xml.etree.cElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET
    root = ET.fromstring(data_xml)
    for child in root:
        data_dict[child.tag] = child.text
    return data_dict
@csrf_exempt
def wechat_notify(request):
    """微信支付结果通知"""
    if request.method == 'POST':
        try:
            # 获取微信支付回调数据
            xml_data = request.body
            wechat_pay = WechatPayAPI()
            
            # 验证签名
            if not wechat_pay.verify_payment(xml_data):
                return HttpResponse('<xml><return_code><![CDATA[FAIL]]></return_code></xml>')
            
            # 解析XML数据
            data = wechat_pay.parse_xml(xml_data)
            
            return HttpResponse('<xml><return_code><![CDATA[FAIL]]></return_code></xml>')
            
        except Exception as e:
            logger.error(f"处理微信支付回调失败: {str(e)}")
            return HttpResponse('<xml><return_code><![CDATA[FAIL]]></return_code></xml>')
    
    return HttpResponse('<xml><return_code><![CDATA[FAIL]]></return_code></xml>')
