"""
URL configuration for mytestsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
# Use include() to add paths from the catalog application
from django.urls import include
# Add URL maps to redirect the base URL to our application
from django.views.generic import RedirectView
# Use static() to add URL mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
]
urlpatterns += [#每当遇到导入函数时django.urls.include()，它都会在指定的结束字符处拆分 URL 字符串，并将剩余的子字符串发送到包含的URLConf模块进行进一步处理
    path('catalog/', include('catalog.urls')),
]
#将第一个参数留空，以暗示 '/'。如果将第一个参数写为 '/'，Django 会在启动开发服务器时给出警告
urlpatterns += [
    path('', RedirectView.as_view(url='catalog/', permanent=True)), 
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Add Django site authentication urls (for login, logout, password management) 会一次性引入 Django 内置的所有认证相关 URL 路由
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
