

#添加构建应用程序时的模式
from django.urls import path
from . import views

urlpatterns = [
     path('', views.index, name='index'),
]
