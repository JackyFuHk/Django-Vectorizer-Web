from django.db.models.signals import post_save
from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.shortcuts import reverse
from django_countries.fields import CountryField
import uuid
from django.utils.text import slugify  
import os
from multiselectfield import MultiSelectField  
from django import forms  
import datetime
from django.contrib.auth.forms import AuthenticationForm  
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')
)

ADDRESS_CHOICES = (
    ('B', 'Billing'),
    ('S', 'Shipping'),
)


###############################################
class ActivateCode(models.Model):
    code = models.CharField(max_length=100, unique=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code


## 用户登录表单
class CustomAuthenticationForm(AuthenticationForm):  
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '邮箱'}))  
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '密码'}))

## 联系我们
class Contact(models.Model):  
    name = models.CharField(max_length=100)  
    email = models.EmailField()  
    is_response = models.BooleanField(default=False)
    content = models.TextField()

    def __str__(self):  
        return self.name

## 博客
class Post(models.Model):  
    title = models.CharField(max_length=200)  
    slug = models.SlugField(unique=True, blank=True, null=True) 
    content = models.TextField()  
    cover_image = models.ImageField(blank=True)
    cover_image_alt = models.CharField(max_length=200,default="White Logo in PixelOpen.COM For Free")  
    short_description = models.TextField(blank=True,null=True)
    post_category = models.CharField(max_length=100,blank=True,null=True)
    post_author = models.CharField(max_length=100,default="PixelOpen Team")
    created_at = models.DateTimeField(auto_now_add=True)  
    updated_at = models.DateTimeField(auto_now=True)  
    view_count = models.PositiveIntegerField(default=0)  
  
    def save(self, *args, **kwargs):  
        if not self.slug:  
            self.slug = slugify(self.title)  
        super().save(*args, **kwargs)  
  
    def __str__(self):  
        return self.title

### 工具
class Tools(models.Model):
    toolname = models.CharField(max_length=200)  
    slug = models.SlugField(unique=True, blank=True, null=True) 
    long_description = models.TextField()  
    cover_image = models.ImageField(blank=True)
    cover_image_alt = models.CharField(max_length=200,default="White Logo in PixelOpen.COM For Free")  
    short_description = models.TextField(blank=True,null=True)

    def save(self, *args, **kwargs):  
        if not self.slug:  
            self.slug = slugify(self.title)  
        super().save(*args, **kwargs)  
  
    def __str__(self):  
        return self.toolname

CONVERTER_CHOICES = (
    ('RGB', 'RGB'),
    ('HEX', 'HEX'),
    ('HSL', 'HSL'),
    ('CMYK', 'CMYK'),
    ('HSV', 'HSV'),
    ('LAB', 'LAB'),
)
class ConverterTools(models.Model):
    converterName = models.CharField(max_length=100)  
    slug = models.SlugField(unique=True, blank=True, null=True) 
    short_description = models.TextField(blank=True,null=True)
    long_description = models.TextField(blank=True,null=True) 

    cover_image = models.ImageField(blank=True)
    cover_image_alt = models.CharField(max_length=200,default="Color Convertor in PixelOpen.COM For Free")  
    
    related_post = models.CharField(max_length=1000,blank=True,null=True)
    change_slut = models.SlugField(unique=True, blank=True, null=True)
    # 输入是
    input_category = models.CharField(choices=CONVERTER_CHOICES, max_length=50)
    # 输出是
    output_category = models.CharField(choices=CONVERTER_CHOICES, max_length=50)

    def save(self, *args, **kwargs):  
        if not self.slug:  
            self.slug = slugify(self.converterName)  
        super().save(*args, **kwargs)  
  
    def __str__(self):  
        return self.converterName

class ColorOptions(models.Model):
    colorName = models.CharField(choices=CONVERTER_CHOICES, max_length=50)
    short_description = models.TextField(blank=True,null=True)
    long_description = models.TextField(blank=True,null=True) 

    cover_image = models.ImageField(blank=True)
    cover_image_alt = models.CharField(max_length=200,default="Color Convertor in PixelOpen.COM For Free")  
    
    related_post = models.TextField(blank=True,null=True)

    # 输入:Red (min: 0, max: 255), Green (min: 0, max: 255), Blue (min: 0, max: 255)
    output = models.TextField(blank=True,null=True)
    # 单位，CMYK是百分号
    unit = models.CharField(max_length=10,blank=True)

    def __str__(self):  
        return self.colorName


class FullFeature(models.Model):
    feature_title = models.CharField(max_length=100)
    feature_content = models.TextField()

    def __str__(self):
        return self.feature_title

class FAQs(models.Model):
    question = models.CharField(max_length=100)
    answer =  models.TextField()

    def __str__(self):
        return self.question


class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    one_click_purchasing = models.BooleanField(default=False)
    name = models.CharField(max_length=100,blank=True)
    # invitation_code = models.CharField(max_length=100,blank=True)
    subscriptionID = models.CharField(max_length=100,blank=True)
    subscriptionEnd = models.DateTimeField(default=timezone.now)
    is_subscription = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
    # stripe_customer_id = models.CharField(max_length=50, blank=True, null=True)
    # one_click_purchasing = models.BooleanField(default=False)
    # 新增加的微信字段
    # nickname = models.CharField(max_length=64, null=True, blank=True)
    # sex = models.PositiveSmallIntegerField(choices=((0, '未知'), (1, '男'), (2, '女')), null=True, blank=True)
    # language = models.CharField(max_length=32, null=True, blank=True)
    # city = models.CharField(max_length=32, null=True, blank=True)
    # province = models.CharField(max_length=32, null=True, blank=True)
    # country = models.CharField(max_length=32, null=True, blank=True)
    # headimgurl = models.URLField(null=True, blank=True)
    # privilege = models.JSONField(default=list, blank=True, null=True)  # 使用可调用的默认值
    # unionid = models.CharField(max_length=128, null=True, blank=True)

    # @classmethod
    # def create_or_update_from_wechat(cls, wechat_data):
    #     user, created = cls.objects.update_or_create(
    #         openid=wechat_data['openid'],
    #         defaults={
    #             'nickname': wechat_data.get('nickname', ''),
    #             'sex': wechat_data.get('sex', 0),
    #             'language': wechat_data.get('language', ''),
    #             'city': wechat_data.get('city', ''),
    #             'province': wechat_data.get('province', ''),
    #             'country': wechat_data.get('country', ''),
    #             'headimgurl': wechat_data.get('headimgurl', ''),
    #             'privilege': wechat_data.get('privilege', []),
    #             'unionid': wechat_data.get('unionid', ''),
    #         }
    #     )
    #     return user
    
    def __str__(self):
        return self.user.username

class Pricing(models.Model):
    item_name = models.CharField(max_length=200)
    currency = models.CharField(max_length=100)
    amount = models.CharField(max_length=100)
    period = models.IntegerField()
    
    def __str__(self):
        return self.item_name

class PricingFaqs(models.Model):
    question = models.CharField(max_length=100)
    answer =  models.TextField()

    def __str__(self):
        return self.question

class OrderHistory(models.Model):
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    transaction_id = models.CharField(max_length=255)
    status = models.CharField(max_length=255)

    def __str__(self):
        return self.transaction_id


class ImageHistory(models.Model):
    #用户名，工具url，原图url，转换后的svg图的字符串，是否已下载，时间。
    user_name = models.CharField(max_length=100)
    tool = models.CharField(max_length=100)

    initial_img = models.CharField(max_length=500)
    svg_content = models.TextField()
    is_download = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)  


    def __str__(self):
        return self.user_name + self.initial_img