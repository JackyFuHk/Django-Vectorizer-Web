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
from algorithm.pngtosvg_v1.main import png2svg,removebg_func,upscale_func,whitelogo_func,outline_func,sam_func
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
def white_logo_image(request):  
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
def pngtosvg(request):  
    if request.method == 'POST':
        data = json.loads(request.body)  
        png_url = data.get('imgsrc')  
        index = data.get('index')
        name = data.get('name')

        svg_content= png2svg(png_url)

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
def removebg(request):
    if request.method == 'POST':
        data = json.loads(request.body)  
        png_url = data.get('imgsrc')  
        index = data.get('index')
        name = data.get('name')

        svg_content= removebg_func(png_url)

        response_data = {  
            'status': 'success',  
            # 'svg_content': svg_content,  # 如果你要返回 SVG 内容  
            'index':index,
            'name':name
        }  
        request.session[name] = svg_content
        
        # 写到 数据库里。用户名，工具url，原图url，转换后的svg图的字符串，是否已下载，时间。
        ImageHistory.objects.create(user_name=request.user.username,tool="removebg", initial_img=png_url,svg_content=svg_content)

        return JsonResponse(response_data)


@csrf_exempt
def upscale(request):
    if request.method == 'POST':
        data = json.loads(request.body)  
        png_url = data.get('imgsrc')  
        index = data.get('index')
        name = data.get('name')
        times = data.get('times')
        svg_content= upscale_func(png_url,times)

        response_data = {  
            'status': 'success',  
            # 'svg_content': svg_content,  # 如果你要返回 SVG 内容  
            'index':index,
            'name':name
        }  
        request.session[name] = svg_content
        
        # 写到 数据库里。用户名，工具url，原图url，转换后的svg图的字符串，是否已下载，时间。
        ImageHistory.objects.create(user_name=request.user.username,tool="upscale", initial_img=png_url,svg_content=svg_content)

        return JsonResponse(response_data)

@csrf_exempt
def whitelogo(request):
    if request.method == 'POST':
        data = json.loads(request.body)  
        png_url = data.get('imgsrc')  
        index = data.get('index')
        name = data.get('name')
        svg_content= whitelogo_func(png_url)

        response_data = {  
            'status': 'success',  
            # 'svg_content': svg_content,  # 如果你要返回 SVG 内容  
            'index':index,
            'name':name
        }  
        request.session[name] = svg_content
        
        # 写到 数据库里。用户名，工具url，原图url，转换后的svg图的字符串，是否已下载，时间。
        ImageHistory.objects.create(user_name=request.user.username,tool="whitelogo", initial_img=png_url,svg_content=svg_content)

        return JsonResponse(response_data)

@csrf_exempt
def outline(request):
    if request.method == 'POST':
        data = json.loads(request.body)  
        png_url = data.get('imgsrc')  
        index = data.get('index')
        name = data.get('name')
        svg_content = outline_func(png_url)

        response_data = {  
            'status': 'success',  
            # 'svg_content': svg_content,  # 如果你要返回 SVG 内容  
            'index':index,
            'name':name
        }  
        request.session[name] = svg_content
        
        # 写到 数据库里。用户名，工具url，原图url，转换后的svg图的字符串，是否已下载，时间。
        ImageHistory.objects.create(user_name=request.user.username,tool="outline", initial_img=png_url,svg_content=svg_content)

        return JsonResponse(response_data)

@csrf_exempt
def sam(request):
    if request.method == 'POST':
        data = json.loads(request.body)  
        logo_url = data.get('logo_url')  
        input_point_list = data.get('input_point_list')
        input_label_list = data.get('input_label_list') 
        name = data.get('name')
        svg_content = sam_func(logo_url,input_point_list,input_label_list)

        response_data = {  
            'status': 'success',  
            'data': svg_content,  
            'name':name
        }  
        request.session[name] = svg_content
        
        # 写到 数据库里。用户名，工具url，原图url，转换后的svg图的字符串，是否已下载，时间。
        ImageHistory.objects.create(user_name=request.user.username,tool="sam", initial_img=logo_url,svg_content=svg_content)

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
    ImageHistory.objects.filter(user_name=request.user.username,is_download=False,tool="png2svg",initial_img=png_url).update(is_download = True)
    return JsonResponse(response_data)

def removebg_download_svg(request):
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
    ImageHistory.objects.filter(user_name=request.user.username,is_download=False,tool="removebg",initial_img=png_url).update(is_download = True)
    return JsonResponse(response_data)

def upscale_download_svg(request):
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
    ImageHistory.objects.filter(user_name=request.user.username,is_download=False,tool="upscale",initial_img=png_url).update(is_download = True)
    return JsonResponse(response_data)

def whitelogo_download_svg(request):
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
    ImageHistory.objects.filter(user_name=request.user.username,is_download=False,tool="whitelogo",initial_img=png_url).update(is_download = True)
    return JsonResponse(response_data)

def outline_download_svg(request):
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
    ImageHistory.objects.filter(user_name=request.user.username,is_download=False,tool="outline",initial_img=png_url).update(is_download = True)
    return JsonResponse(response_data)

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
    
def removebg_view(request):
    if request.user.is_authenticated:
        imagehistory = ImageHistory.objects.filter(user_name=request.user.username,is_download=False,tool="removebg")

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

        return render(request,'removebg.html',{"imagehistory":imagehistory,"imagehistory_json":json.dumps(myall)})
    else:
        return render(request,'removebg.html')

def upscale_view(request):
    if request.user.is_authenticated:
        imagehistory = ImageHistory.objects.filter(user_name=request.user.username,is_download=False,tool="upscale")

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

        return render(request,'upscale.html',{"imagehistory":imagehistory,"imagehistory_json":json.dumps(myall)})
    else:
        return render(request,'upscale.html')

def whitelogo_view(request):
    if request.user.is_authenticated:
        imagehistory = ImageHistory.objects.filter(user_name=request.user.username,is_download=False,tool="whitelogo")

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

        return render(request,'whitelogo.html',{"imagehistory":imagehistory,"imagehistory_json":json.dumps(myall)})
    else:
        return render(request,'whitelogo.html')

def outline_view(request):
    if request.user.is_authenticated:
        imagehistory = ImageHistory.objects.filter(user_name=request.user.username,is_download=False,tool="outline")

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

        return render(request,'outline.html',{"imagehistory":imagehistory,"imagehistory_json":json.dumps(myall)})
    else:
        return render(request,'outline.html')

def sam_view(request):
    if request.user.is_authenticated:
        imagehistory = ImageHistory.objects.filter(user_name=request.user.username,is_download=False,tool="sam")

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

        return render(request,'sam.html',{"imagehistory":imagehistory,"imagehistory_json":json.dumps(myall)})
    else:
        return render(request,'sam.html')

@csrf_exempt
def upload_image(request):
    if request.method == 'POST':  
        # 获取文件数据  
        if 'file' in request.FILES:  
            uploaded_file = request.FILES['file']  
        
            image = Image.open(uploaded_file).convert('RGBA')
            
            png_addr = os.path.join(settings.MEDIA_ROOT, "PixelOpen_PNGTOSVG_Result_{}_{}.png".format(datetime.now().strftime("%Y%m%d-%H%M%S"),uuid.uuid4()))  
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
