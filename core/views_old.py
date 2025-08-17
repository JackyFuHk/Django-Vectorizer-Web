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
from .models import CustomAuthenticationForm
import xml.etree.ElementTree as ET
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.contrib.auth import authenticate  
from django.views.decorators.csrf import csrf_exempt
import re
import requests
from algorithm.pngtosvg_v1.main import png2svg
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
from .models import Pricing,PricingFaqs
from django.views.generic import TemplateView

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

# 微信登录
def user_login_wechat(request):
    
    # 获取授权
    wechat_auth_url = f'https://open.weixin.qq.com/connect/oauth2/authorize?appid={settings.SOCIAL_AUTH_WEIXIN_KEY}&redirect_uri={settings.WECHAT_REDIRECT_URI}&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect'
    return HttpResponseRedirect(wechat_auth_url)


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
    return render(request, 'account.html',{'user': user_info})  

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
        password2 = str(random.randint(000000,999999))
        certification_code = data.get('code')
        print(certification_code,request.session['certification_code'])
        if certification_code != request.session['certification_code']:
            return HttpResponse('certification code is not correct.')  
        print(email,certification_code)
        if User.objects.filter(username=email):
            user =User.objects.filter(username=email)[0]
            backend = 'django.contrib.auth.backends.ModelBackend'
    
            user.backend = backend  
            login(request, user)
        else:
            user = User.objects.create_user(username=email, email=email, password=password2)
            user.save()
            backend = 'django.contrib.auth.backends.ModelBackend'
    
            user.backend = backend 
            login(request, user) 
        return JsonResponse({'code':'200','status': 'success', 'message': '账户已创建'})  

def generate_verification_code(length=6):  
    """生成一个随机的验证码"""  
    return ''.join(random.choices(string.digits, k=length))  
   
def register_send_certification(request):
  
    if request.method == 'POST': 
        data = json.loads(request.body)  
        email = data.get('email')  
        if email:  
            # 生成验证码  
            verification_code = generate_verification_code(length=4)  
            request.session['certification_code'] = verification_code
            SMS.main(phone_number=email,code2=verification_code)  
            
            return JsonResponse({'code':'200','status': 'success', 'message': '验证码已发送'})  
      
    return JsonResponse({'code':'400','status': 'error', 'message': '无效的请求'}, status=400)  

import pytz
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
    


from urllib.parse import quote
from django.http import HttpResponseRedirect
from .models import UserProfile
def user_login(request):
    appid = settings.WECHAT_APPID
    redirect_uri = quote(settings.WECHAT_REDIRECT_URI)
    url = f"https://open.weixin.qq.com/connect/qrconnect?appid={appid}&redirect_uri={redirect_uri}&response_type=code&scope=snsapi_login&state=STATE#wechat_redirect"
    return HttpResponseRedirect(url)

# def logout_view(request):
#     logout(request)
#     # 重定向到登录页面或者主页
#     return redirect('account')

def wechat_login_callback(request):
    # 授权成功，回调

    # 通过code换取网页授权access_token
    code = request.GET.get('code')
    appid = settings.SOCIAL_AUTH_WEIXIN_KEY
    secret = settings.SOCIAL_AUTH_WEIXIN_SECRET
    
    url = f'https://api.weixin.qq.com/sns/oauth2/access_token?appid={appid}&secret={secret}&code={code}&grant_type=authorization_code'
    response = requests.get(url)
    data = response.json()

    access_token = data.get('access_token')
    openid = data.get('openid')
    url = f'https://api.weixin.qq.com/sns/userinfo?access_token={access_token}&openid={openid}'
    response = requests.get(url)
    response.encoding = 'utf-8'  # 设置响应内容的编码为UTF-8
    user_info = response.json()

    defaults={
            'nickname': user_info.get('nickname', ''),
            'sex': user_info.get('sex', 0),
            'language': user_info.get('language', ''),
            'city': user_info.get('city', ''),
            'province': user_info.get('province', ''),
            'country': user_info.get('country', ''),
            'headimgurl': user_info.get('headimgurl', ''),
            'privilege': user_info.get('privilege', []),
            'unionid': user_info.get('unionid', ''),
        }
    # 创建或者更新用户信息
    user = User.objects.create_user(username=defaults["nickname"], email="{}@gmail.com".format(random.randint(00000000,99999999)), password=defaults['unionid'])
    

    user_profile = UserProfile.objects.create(user=user)

    user_profile.nickname = defaults['nickname']
    user_profile.sex = defaults['sex']
    user_profile.language = defaults['language']
    user_profile.city = defaults['city']
    user_profile.province = defaults['province']
    user_profile.country = defaults['country']
    user_profile.headimgurl = defaults['headimgurl']
    user_profile.unionid = defaults['unionid']
    user_profile.privilege = defaults['privilege']
    user.save()
    user_profile.save()
    # 选择要登录的后端认证系统，这里可以选择Django自带的，也可以选择微信的
    backend = 'django.contrib.auth.backends.ModelBackend'
    # backend = 'allauth.account.auth_backends.AuthenticationBackend'
    user.backend = backend  # 设置用户实例的后端属性
    login(request, user, backend=backend)  # 登录用户，传入backend参数

    # 这里我随便写了一个url名称
    return redirect("/")



def register_wechat(request):
    token_url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={settings.SOCIAL_AUTH_WEIXIN_KEY}&secret={settings.SOCIAL_AUTH_WEIXIN_SECRET}'
   
    response = requests.get(token_url)
    data = response.json()

    access_token = data.get('access_token')


    url = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={}".format(access_token)
    data = {
        "expire_seconds": 300,
        "action_name": "QR_SCENE",
        "action_info": {
            "scene": {
                "scene_id": 1
            }
        }
    }
    ret = requests.post(url=url, data=json.dumps(data))
    data = json.loads(ret.content)
    print(data)
    ticket = data.get('ticket')
    
    return render(request,'login_wechat.html',{'loginqrcode':'https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={}'.format(ticket)})

def xml2Json(xml):
    root = ET.fromstring(xml)
    ret = {}
    # 遍历xml文档的第二层
    for child in root:
        # 第二层节点的标签名称和属性
        ret[child.tag] = child.text
        # 遍历xml文档的第三层
        for children in child:
            # 第三层节点的标签名称和属性
            ret[child.tag] = child.text
    return ret

def get_wx_msg(request):
    signature = request.GET.get('signature')
    echostr = request.GET.get('echostr')
    timestamp = request.GET.get('timestamp')
    nonce = request.GET.get('nonce')

    return HttpResponse(echostr)


import hashlib
import xml.etree.ElementTree as ET
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
 
WECHAT_TOKEN = 'png2svgVECTORIZER888'  # 替换为你的微信 Token
 
 
def check_signature(token, signature, timestamp, nonce):
    """
    校验微信服务器签名
    """
    tmp_list = [token, timestamp, nonce]
    tmp_list.sort()
    list_str = ''.join(tmp_list).encode('utf-8')
	
    sha1 = hashlib.sha1()
    sha1.update(list_str)
    # map(sha1.update, list_para)
    # 加密
    hashcode = sha1.hexdigest()

    return hashcode == signature

@method_decorator(csrf_exempt, name='dispatch')
class WeChatView(View):
    def get(self, request, *args, **kwargs):
        """
        处理微信服务器验证 GET 请求
        """
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        echostr = request.GET.get('echostr')
        if check_signature(settings.WECHAT_MSG_TOKEN, signature, timestamp, nonce):
            return HttpResponse(echostr)
 
    def post(self, request, *args, **kwargs):
        """
        处理微信服务器发送的消息 POST 请求
        """
        xml_data = request.body.decode('utf-8')
        # root = ET.fromstring(xml_data)
        ret = xml2Json(xml_data)
        open_id = ret.get('FromUserName')
        
        

        logger.error("xmldata: %s ", ret) 

        '''
        xmldata: {'ToUserName': 'gh_889fde3766af', 'FromUserName': 'oktzk6se0EvQeZvsXKBbSoJgToU8', 'CreateTime': '1731827931', 'MsgType': 'event', 'Event': 'SCAN', 'EventKey': '1', 'Ticket': 'gQGE8DwAAAAAAAAAAS5odHRwOi8vd2VpeGluLnFxLmNvbS9xLzAyS1puZVUyaXNmQUcxODNxVnhEMVAAAgTXmDlnAwQsAQAA'}

        '''
        if ret.get('MsgType') == 'event':
            if ret.get('Event') == 'SCAN':
                token_url = f'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={settings.SOCIAL_AUTH_WEIXIN_KEY}&secret={settings.SOCIAL_AUTH_WEIXIN_SECRET}'
   
                response = requests.get(token_url)
                data = response.json()

                access_token = data.get('access_token')
                
                
                
                logger.error("access_token: %s ", access_token) 
                
                logger.error("access_token: %s ", open_id) 
                url = f"https://api.weixin.qq.com/cgi-bin/user/info?access_token={access_token}&openid={open_id}&lang=zh_CN"
                res = requests.get(url)
                # print(res.json())
                user_info = res.json()

                
                logger.error("userinfo: %s ", user_info) 
                defaults={
                    'nickname': user_info.get('nickname', ''),
                    'sex': user_info.get('sex', 0),
                    'language': user_info.get('language', ''),
                    'city': user_info.get('city', ''),
                    'province': user_info.get('province', ''),
                    'country': user_info.get('country', ''),
                    'headimgurl': user_info.get('headimgurl', ''),
                    'privilege': user_info.get('privilege', []),
                    'unionid': user_info.get('unionid', ''),
                    'openid':user_info.get('openid', ''),
                }
                # 创建或者更新用户信息

                try:
                    user = User.objects.get(username=defaults["openid"])
                except:
                    user = User.objects.create_user(username=defaults["openid"], email="{}@gmail.com".format(random.randint(00000000,99999999)), password=defaults['unionid'])
                
                    user_profile = UserProfile.objects.create(user=user)

                    user_profile.nickname = defaults['nickname']
                    user_profile.sex = defaults['sex']
                    user_profile.language = defaults['language']
                    user_profile.city = defaults['city']
                    user_profile.province = defaults['province']
                    user_profile.country = defaults['country']
                    user_profile.headimgurl = defaults['headimgurl']
                    user_profile.unionid = defaults['unionid']
                    user_profile.privilege = defaults['privilege']
                    user.save()
                    user_profile.save()


                # 选择要登录的后端认证系统，这里可以选择Django自带的，也可以选择微信的
                backend = 'django.contrib.auth.backends.ModelBackend'
                # backend = 'allauth.account.auth_backends.AuthenticationBackend'
                user.backend = backend  # 设置用户实例的后端属性
                login(request, user, backend=backend)  # 登录用户，传入backend参数

                # 这里我随便写了一个url名称
                return redirect("/")












        # # 提取消息内容，这里只是示例，具体提取方式根据 XML 结构而定
        # from_user_name = root.find('FromUserName').text
        # to_user_name = root.find('ToUserName').text
        # msg_type = root.find('MsgType').text
        # content = root.find('Content').text if msg_type == 'text' else ''

        # # 根据消息类型进行处理
        # if msg_type == 'text':
        #     # 回复文本消息
        #     reply_xml = f"""
        #     <xml>
        #         <ToUserName><![CDATA[{from_user_name}]]></ToUserName>
        #         <FromUserName><![CDATA[{to_user_name}]]></FromUserName>
        #         <CreateTime>{int(time.time())}</CreateTime>
        #         <MsgType><![CDATA[text]]></MsgType>
        #         <Content><![CDATA[你发送的是: {content}]]></Content>
        #     </xml>
        #     """
            
        return HttpResponse('success')
 
        # 默认回复
        return HttpResponseBadRequest('Unsupported message type')











#########################################################################
from django.urls import reverse
from django.shortcuts import render
from django.conf import settings

def get_order_id():
    # 获取当前的日期和时间  
    now = datetime.datetime.now()  
    
    # 格式化日期和时间为所需的字符串格式  
    formatted_now = now.strftime('%Y%m%d%H%M%S')  
    
    # 生成三个随机数字  
    random_numbers = ''.join(str(random.randint(0, 9)) for _ in range(3))  
    
    # 组合日期时间字符串和随机数字字符串  
    result_string = formatted_now + random_numbers  
    return result_string



def pricing(request):
    price_table = Pricing.objects.all()

    faqs = PricingFaqs.objects.all()
    faqs_chunked = [faqs[i:i+1] for i in range(0, len(faqs), 1)] 

    return render(request, "pricing.html",{'faqs':faqs_chunked,'price':price_table})




############################################################################
from django.http import JsonResponse
from PIL import Image
import cv2
import numpy as np
from algorithm.reverseImage import whiteningLogo
from algorithm.borderFunc import dropBlankBorder,expandBorder
import base64
from algorithm.potracyImage import fileVectorize,imgVectorize
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
def upload_image(request):  
    if request.method == 'POST':  
        # 获取文件数据  
        if 'file' in request.FILES:  
            uploaded_file = request.FILES['file']  
            image = Image.open(uploaded_file)
            opencv_image_bgr = cv2.cvtColor(np.array(image) , cv2.COLOR_RGB2BGRA)
            opencv_image_bgr = expandBorder(opencv_image_bgr,expands=20)
            left_image = dropBlankBorder(opencv_image_bgr,expand=1)
            right_image = whiteningLogo(opencv_image_bgr,coloring_logo="#FFFFFF")

            left_png_url = os.path.join(settings.MEDIA_ROOT, "PixelOpen_White_Logo_Origin_{}.png".format(datetime.now().strftime("%Y%m%d-%H%M%S")))  
            cv2.imwrite(left_png_url,left_image)  
            right_png_url = os.path.join(settings.MEDIA_ROOT, "PixelOpen_White_Logo_Result_{}.png".format(datetime.now().strftime("%Y%m%d-%H%M%S")))  
            cv2.imwrite(right_png_url,right_image)  
            right_image_svg = imgVectorize(right_image)
            
            left_image = settings.MEDIA_URL + os.path.relpath(left_png_url, settings.MEDIA_ROOT)  
            right_image = settings.MEDIA_URL + os.path.relpath(right_png_url, settings.MEDIA_ROOT)  

        else:  
            uploaded_file = None  
        
        
        # 构建响应消息  
        response_data = {  
            'message': 'Image clicked! This is the response from the server.',  
            'left-image': left_image, 
            'right-image': right_image,
            'right-image-svg':right_image_svg
        }  
  
        # 返回 JSON 响应  
        return JsonResponse(response_data)  
    else:  
        # 如果不是 POST 请求，返回错误消息或重定向到表单页面  
        return JsonResponse({'message': 'Invalid request method. Only POST requests are allowed.'}, status=400)
@csrf_exempt
def editor(request):
    leftImage = request.GET.get('originimage',staticfiles_storage.url('img/homeImage/pixelopen_demo.png'))
    rightImage = request.GET.get('resultimage', staticfiles_storage.url('img/homeImage/pixelopen_black_and_white_demo2.svg'))
    right_image_png = request.GET.get('resultimage', staticfiles_storage.url('img/homeImage/pixelopen_black_and_white_demo.png'))
    # 跳转到编辑器时，转成svg。
    if not rightImage.endswith('svg'):
        rightImage = fileVectorize(rightImage)
    else:
        with open(r'static_in_env/img/homeImage/pixelopen_black_and_white_demo2.svg',"r") as f:
            rightImage = f.read()
        # svg_file_path = os.path.join(settings.MEDIA_ROOT, "{}.svg".format(uuid.uuid4()))  
        # with open(svg_file_path, 'w', encoding='utf-8') as f:  
        #     f.write(svg_data)  
        # rightImage = settings.MEDIA_URL + os.path.relpath(svg_file_path, settings.MEDIA_ROOT)  
        # return render(request,  "editor.html", {"leftImage":leftImage,"rightImage":svg_data})

    return render(request,  "editor.html", {"leftImage":leftImage,"rightImage":rightImage,"right_image_png":right_image_png})

@csrf_exempt
def svg2png(request):
    if request.method == 'POST': 
        data = json.loads(request.body)  
        png_url = data.get('png_url')  
        png_url = settings.DOMAIN_NAME + png_url

        svg_content,svg_width,svg_height = png2svg(png_url)
        # svg_content = settings.MEDIA_URL + os.path.relpath(svg_content, settings.MEDIA_ROOT)  
        # 由于这是一个示例，我们直接返回一个模拟的响应  
        response_data = {  
            'status': 'success',  
            'svg_content': svg_content,  # 如果你要返回 SVG 内容  
            'width':svg_width,
            'height':svg_height,
            # 'svg_url': some_svg_url,     # 如果你要返回 SVG 的 URL  
        }  
        request.session['user_svg_data'] = svg_content  
        return JsonResponse(response_data)

@csrf_exempt
def download_svg(request):
    my_variable = request.session.get('user_svg_data')
    

    response_data = {
        "data":my_variable
    }
    return JsonResponse(response_data)

@csrf_exempt
def home_download_svg(request):
    data = json.loads(request.body)  
    index = data.get('name')
    my_variable = request.session.get(index)
    

    response_data = {
        "data":my_variable
    }
    return JsonResponse(response_data)


@csrf_exempt
def upload_image_pngtosvg2(request):  
    if request.method == 'POST':  
        # 获取文件数据  
        if 'file' in request.FILES:  
            uploaded_file = request.FILES['file']  
            image = Image.open(uploaded_file).convert('RGBA')
            png_addr = os.path.join(settings.MEDIA_ROOT, "PixelOpen_PNGTOSVG_Result_{}.png".format(datetime.now().strftime("%Y%m%d-%H%M%S")))  
            image.save(png_addr)
            
            # opencv_image_bgr = cv2.cvtColor(np.array(image) , cv2.COLOR_RGB2BGRA)
            # svg_addr = os.path.join(settings.MEDIA_ROOT, "PixelOpen_PNGTOSVG_Result_{}.svg".format(datetime.now().strftime("%Y%m%d-%H%M%S")))  
            svg_url = settings.MEDIA_URL + os.path.relpath(png_addr, settings.MEDIA_ROOT)  
            
            if 'http' not in svg_url:
                png_url = settings.DOMAIN_NAME + svg_url
            else:
                png_url = svg_url
            svg_content,svg_width,svg_height = png2svg(png_url)
            # svg_content = settings.MEDIA_URL + os.path.relpath(svg_content, settings.MEDIA_ROOT)  
            # 由于这是一个示例，我们直接返回一个模拟的响应  
            response_data = {  
                'status': 'success',  
                'svg_content': svg_content,  # 如果你要返回 SVG 内容  
                'width':svg_width,
                'height':svg_height,
                # 'svg_url': some_svg_url,     # 如果你要返回 SVG 的 URL  
            }  
            # 设置会话变量  

            request.session['user_svg_data'] = svg_content  
            


            return JsonResponse(response_data)
        else:  
            uploaded_file = None  
        
        
        # 构建响应消息  
        response_data = {  
            'message': 'Image clicked! This is the response from the server.',  
            'user_png':svg_url
        }  
  
        # 返回 JSON 响应  
        return JsonResponse(response_data)  
    else:  
        # 如果不是 POST 请求，返回错误消息或重定向到表单页面  
        return JsonResponse({'message': 'Invalid request method. Only POST requests are allowed.'}, status=400)



@csrf_exempt
def upload_image_pngtosvg(request):  
    if request.method == 'POST':  
        # 获取文件数据  
        if 'file' in request.FILES:  
            uploaded_file = request.FILES['file']  
        
            image = Image.open(uploaded_file).convert('RGBA')
            
            png_addr = os.path.join(settings.MEDIA_ROOT, "PixelOpen_PNGTOSVG_Result_{}_{}.png".format(datetime.now().strftime("%Y%m%d-%H%M%S"),uuid.uuid4()))  
            image.save(png_addr)
            
            # opencv_image_bgr = cv2.cvtColor(np.array(image) , cv2.COLOR_RGB2BGRA)
            # svg_addr = os.path.join(settings.MEDIA_ROOT, "PixelOpen_PNGTOSVG_Result_{}.svg".format(datetime.now().strftime("%Y%m%d-%H%M%S")))  
            svg_url = settings.MEDIA_URL + os.path.relpath(png_addr, settings.MEDIA_ROOT)  
            
            if 'http' not in svg_url:
                png_url = settings.DOMAIN_NAME + svg_url
            else:
                png_url = svg_url
          
            svg_content,_,_ = png2svg(png_url)
            request.session[uploaded_file.name] = svg_content
   
        else:  
            uploaded_file = None  
        
        
        # 构建响应消息  
        response_data = {  
            'message': 'Image clicked! This is the response from the server.',  
            # 'user_png':svg_content,
            'name':uploaded_file.name
        }  
  
        # 返回 JSON 响应  
        return JsonResponse(response_data)  
    else:  
        # 如果不是 POST 请求，返回错误消息或重定向到表单页面  
        return JsonResponse({'message': 'Invalid request method. Only POST requests are allowed.'}, status=400)

@csrf_exempt
def pngtosvgCanvas(request):
    svgImage = request.GET.get('svg', staticfiles_storage.url('img/pngtosvg/demo.svg'))

    if "png" in svgImage:
        # response = requests.get(svgImage)  
        # svg_content = response.content.decode('utf-8')
        svg_content = svgImage

    else:
        with open(svgImage) as f:
            svg_content = f.read()
    
    return render(request,  "pngtosvgcanvas.html", {"rightImage":svg_content})


# 删除文本
def delete_file(request):  
    media_root = settings.MEDIA_ROOT  
    cutoff_time = datetime.now() - timedelta(hours=1)  
    cutoff_timestamp = cutoff_time.timestamp()  

    for root, dirs, files in os.walk(media_root):  
        for file in files:  
            if file.endswith('svg') or file.endswith('png'):
                file_path = os.path.join(root, file)  
                try:  
                    file_creation_time = os.path.getctime(file_path)  
                    if file_creation_time < cutoff_timestamp:  
                        os.remove(file_path)  
                except Exception as e:  
                    pass
    return render(request,  "editor.html")

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

def colorLimitedDict(input_string,unit):

    pattern = r'(\w+)\s*\((min:\s*\d+),\s*(max:\s*\d+)\)'  
  
    # 使用 findall 方法找到所有匹配项  
    matches = re.findall(pattern, input_string)  
    
    # 初始化一个空字典来存储结果  
    result_dict = {}  
    
    # 遍历匹配项并创建字典  
    i=0
    init = "("
    for match in matches:  
        color_name = match[0].capitalize()  # 将颜色名称首字母大写  
        min_value = match[1].split(': ')[1]  # 获取 min 值  
        max_value = match[2].split(': ')[1]  # 获取 max 值  
        # 将 min 和 max 存储在一个内部字典中  
        inner_dict = {'min': min_value, 'max': max_value,'name':input_string.split(';')[i]}  # 这里将值转换为整数  
        # 将内部字典添加到结果字典中  
        result_dict[color_name] = inner_dict  
        i+=1
        init+="0"+ unit+","
    init=init[:-1] + ')'
    return result_dict,init
def converter(request,slug):
    main_info = {}
    input = {}
    output = {}

    transferto = ConverterTools.objects.filter(slug=slug)
    colorstypefrom = ColorOptions.objects.all()
    
    for transfer in transferto:
        main_info["title"] = transfer.converterName
        main_info['subtitle'] = transfer.short_description
        main_info['description'] = transfer.long_description.split('<br>')
        main_info['image'] = transfer.cover_image
        main_info['image_alt'] = transfer.cover_image_alt
        main_info['related_post'] = transfer.related_post
        main_info["change_slut"] = transfer.change_slut
        input_category = transfer.input_category
        output_category = transfer.output_category
    for colortype in colorstypefrom:  
        if colortype.colorName == input_category:
            input["name"] = colortype.colorName
            input["short_description"] = colortype.short_description
            input["long_description"] = colortype.long_description
            input["cover_image"] = colortype.cover_image
            input["cover_image_alt"] = colortype.cover_image_alt
            input['related_post'] = colortype.related_post
            input['type'] = colortype.output.split(';')
            input['unit'] = colortype.unit
            input['output_limit'] = colorLimitedDict(colortype.output,colortype.unit)[0]
            input['input_init'] = colorLimitedDict(colortype.output,colortype.unit)[1]
        if colortype.colorName == output_category:
            output["name"] = colortype.colorName
            output["short_description"] = colortype.short_description
            output["long_description"] = colortype.long_description
            output["cover_image"] = colortype.cover_image
            output["cover_image_alt"] = colortype.cover_image_alt
            output['related_post'] = colortype.related_post
            output['type'] = colortype.output.split(';')
            output['unit'] = colortype.unit
            output['output_limit'] = colorLimitedDict(colortype.output,colortype.unit)[0]
            input['output_init'] = colorLimitedDict(colortype.output,colortype.unit)[1]
    return render(request, 'converter.html', {'main_info': main_info,'input':input,'output':output})


# 首页

def homeView(request):
    full_features = FullFeature.objects.all()
    # 将 full_features 分割成每三个一组  
    features_chunked = [full_features[i:i+3] for i in range(0, len(full_features), 3)]  
   
    faqs = FAQs.objects.all()
    faqs_chunked = [faqs[i:i+2] for i in range(0, len(faqs), 2)] 
    return render(request, "home.html",{'full_features':features_chunked,'faqs':faqs_chunked})