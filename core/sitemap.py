from django.contrib.sitemaps import Sitemap
from django.utils import timezone
from django.urls import reverse
from .models import Post,Tools

class MyPostSitemap(Sitemap):
    def items(self):
        return Post.objects.all()

    def location(self, item):
        return '/blogs/%s' % item.slug


    def lastmod(self, item):
        # Set last modified date as current time
        return timezone.now()

class MyToolSitemap(Sitemap):
    def items(self):
        return Tools.objects.all()

    def location(self, item):
        return '/editor/%s' % item.slug

    def lastmod(self, item):
        # Set last modified date as current time
        return timezone.now()
    
class StaticViewSitemap(Sitemap):
    priority = 0.7
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        # 列出你想要包含在站点地图中的URL名称  
        return [  
            '/',  # 根路径和/en/都映射到同一个视图，但通常只包含一个 
            '/home/',  
            '/support/',  # 博客列表  
            '/about-us/',  # 联系我们  
            '/policies/terms/',  # 条款政策  
            '/policies/privacy/',  # 隐私政策  
        ]

    def location(self, item):
        return item
    