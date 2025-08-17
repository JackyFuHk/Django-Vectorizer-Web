from random import Random  # 用于生成随机码
from django.core.mail import send_mail  # 发送邮件模块
from django.conf import settings    # setting.py添加的的配置信息

import datetime


# 生成随机字符串
def random_str(randomlength=8):
    """
    随机字符串
    :param randomlength: 字符串长度
    :return: String 类型字符串
    """
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User

def verify_email(request, token):
    try:
        user = User.objects.get(email_verification_token=token)
        user.is_active = True
        user.save()
        messages.success(request, 'Your email has been verified!')
    except User.DoesNotExist:
        messages.error(request, 'Invalid verification link.')
    return redirect('/')

from django.core.mail import send_mail

def send_verification_email(user_email, verification_link):
    subject = 'Please verify your email'
    message = f'Click the following link to verify your email: {verification_link}'
    send_mail(
        subject=subject,
        message=message,
        from_email='support@pixelopen.com',
        recipient_list=[user_email],
    )

from django.urls import reverse

def generate_verification_link(request, user_id):
    token = random_str()
    user = User.objects.get(id=user_id)
    user.email_verification_token = token
    user.save()
    verification_link = request.build_absolute_uri(reverse('verify_email', args=[token]))
    return verification_link