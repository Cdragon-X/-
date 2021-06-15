"""Store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, re_path
from index import views
# 当前应用名称
app_name = "index"
urlpatterns = [
    re_path("^$", views.index, name="index"),
    re_path("^login/$", views.IndexView.as_view(), name="login"),
    re_path("^register/$", views.ReView.as_view(), name="register"),
    re_path("^search/$", views.search, name="search"),
    re_path("^change_user/$", views.change_user, name="change_user"),
    re_path("^helloword/$", views.hello_word),
    path("slideDown/",views.slideDown)
]
