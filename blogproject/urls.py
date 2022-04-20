"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from blog.feeds import AllPostsRssFeed
from login import views
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings

from .settings import MEDIA_ROOT

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'', include('blog.urls')),
    path(r'index/', include('blog.urls')),
    path(r'', include('comments.urls')),
    path(r'all/rss/', AllPostsRssFeed(), name='rss'),

    path(r'login/', views.login),
    path(r'register/', views.register),
    path(r'logout/', views.logout),
    path(r'captcha/', include('captcha.urls')),  # 验证码
    path(r'profile/', views.user_profile),
    path(r'profile_edit/',views.user_edit),

    #搜索
    # 添加search的url映射
    # path('search/',include('haystack.urls')),
    # path('blog/', include("apps.news.urls")),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
