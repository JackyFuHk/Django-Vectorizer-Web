from django.urls import path,include
from . import views
from django.views.static import serve as static_serve  # 注意这里引入的与上面的不同
from django.urls import re_path
from django.contrib.staticfiles.views import serve
from django.contrib.sitemaps.views import sitemap
from .sitemap import MyPostSitemap,MyToolSitemap,StaticViewSitemap
from django.contrib.sites.models import Site  


# 在你的 Django shell 或者一个管理脚本中运行  
site = Site.objects.get(id=1)  
site.domain = 'vectorizer.cn'  # 替换为你的实际域名  
site.name = 'vectorizer.cn for Bitmap to Vector Image,convert png to svg'    # 可选，设置站点名称  
site.save()

sitemaps = {  
    'articles': MyPostSitemap,
    'staticview': StaticViewSitemap,
}
app_name = 'core'
def return_static(request, path, insecure=True, **kwargs):
  return serve(request, path, insecure, **kwargs)

urlpatterns = [

    # path('login/', views.login_view, name='login'),  
    path('home/',  views.homeView, name='home'),  
    # path('logout/', views.logout_view, name='logout'), 
    path('register/', views.register_view, name='register'),  
    path('register/send_certification/',views.register_send_certification,name='send_email'),
    path('register/create_user/', views.register, name='register'),  
    path('reset/',views.reset_view, name='reset password'),
    path('reset/send_certification/',views.register_send_certification,name='send_email'),
    path('reset/reset_psw/',views.reset, name='reset password'),
    path('login/', views.login_view, name='user_login'),
    path('is_subscription/',views.is_subscription,name='is_subscription'),

    path('tool/pngtosvg/',views.pngtosvg_view,name='pngtosvg'),
    path('api/',views.api_view,name='api'),
    path('api/order/make/', views.make_order, name='make_order'),
    path('wechat/notify/', views.wechat_notify, name='wechat_notify'),
    path('recharge/',views.recharge,name='recharge'),
    # path('api/upload/',views.upload_image,name='upload_image'),
    # path('sendsms/',views.sendsms,name='sendsms'),
    # path('dell/',views.delete_imagehistory,name='delete_imagehistory'),
    # path('tool/removebg/',views.removebg_view,name='removebg'),
    # path('tool/upscale/',views.upscale_view,name='upscale'),
    # path('tool/whitelogo/',views.whitelogo_view,name='whitelogo'),
    # path('tool/outline/',views.outline_view,name='outline'),
    # path('tool/pickpattern/',views.sam_view,name='sam'),
    # path('register/wechat/',views.register_wechat,name='wechat register'),
    # path('wx-server/msg/',WeChatView.as_view(),name='get wx message'),

    
    # path('login_wechat/',views.user_login_wechat,name='wechat_login'),
    path('logout/', views.logout_view, name='logout'),
    # path('wechat/callback/', views.wechat_login_callback, name='wechat_callback'),

    path('account/',views.account_view,name='account'),
    # path('subscribe/',views.pricing,name='price'),
    # path('/payment/paypal/',views.payment_paypal,name='paypal'),
    # path('/payment/alipay/',include('paypal.standard.ipn.urls'),views.payment_alipay,name='alipay'),
    # path('/paypal-return/', views.PaypalReturnView.as_view(), name='paypal-return'),
    # path('/paypal-cancel/', views.PaypalCancelView.as_view(), name='paypal-cancel'),

    path('getCode/',views.getActivateCode,name='get_code'),
    
    path('',  views.homeView, name='home'),
    path('upload-image/',views.upload_image,name='upload'),
    path('pngtosvg/', views.pngtosvg, name='pngtosvg'),
    # path('removebg/',views.removebg,name='removebg'),
    # path('upscale/',views.upscale,name='upscale'),
    # path('whitelogo/',views.whitelogo,name='whitelogo'),
    # path('outline/',views.outline,name='outline'),
    # path('sam/',views.sam,name='sam'),

    # path('upload-image/whitelogo/', views.white_logo_image, name='white_logo_image'),
    # path('upload-image/pngtosvg/', views.upload_image_pngtosvg, name='upload_image_pngtosvg'),
  
    # path('upload/pngtosvg/', views.upload_image_pngtosvg2, name='upload_image_pngtosvg2'),
    # path('download_svg/', views.download_svg, name='download_svg'),
    path('download_svg2/', views.home_download_svg, name='download_svg'),
    # path('removebg_download_svg/',views.removebg_download_svg,name='removebg_download_svg'),
    # path('upscale_download_svg/',views.upscale_download_svg,name='upscale_download_svg'),
    # path('whitelogo_download_svg/',views.whitelogo_download_svg,name='whitelogo_download_svg'),
    # path('outline_download_svg/',views.outline_download_svg,name='outline_download_svg'),
    # path('editor/whitelogo/', views.editor, name='editor'),
    # path('editor/pngtosvg/', views.pngtosvgCanvas, name='pngtosvg'),
    path('get-user-info/',views.home_view,name='home_view'),
    # path('delete-file/', views.delete_file, name='delete_file'),
    path('support/', views.contact_view, name='contact'),
    path('about-us/', views.about_us, name='about_us'),
    path('author/',views.author_view,name='author'),
    path('blogs/', views.post_list, name='post_list'),  
    path('blogs/<slug:slug>/', views.post_detail, name='post_detail'),
    path('policies/terms/', views.policy_term, name='policy_term'),  
    path('policies/privacy/', views.policy_privacy, name='policy_privacy'),  
    re_path(r'^static/(?P<path>.*)$', return_static, name='static'), # 添加这行
    re_path(r'^static/(?P<path>.*)$', static_serve, name='static'), # 添加这行
    path("sitemap.xml", sitemap,{"sitemaps": sitemaps},name="django.contrib.sitemaps.views.sitemap",), # sitemap
     
    # path('convert/<slug:slug>/', views.converter, name='color_converter'),  
    path('i18n/', include('django.conf.urls.i18n')),
  
]


