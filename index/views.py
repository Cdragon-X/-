import json

from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View

from database.models import *

# Create your views here.

# 热门商品
hot_li = hot_com()
# 全部音箱
spk_li = spk_com()


# 主页
def index(request):
    return render(request, "index/index.html", {"com_type": com_type(),
                                                "hot_li": hot_li,
                                                "spk_li": spk_li
                                                })


# 导入图形验证码模块
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url


# 创建验证码
def captcha():
    hashkey = CaptchaStore.generate_key()  # 验证码答案
    image_url = captcha_image_url(hashkey)  # 验证码地址
    captcha = {'hashkey': hashkey, 'image_url': image_url}
    return captcha


# # 刷新验证码
# def refresh_captcha(request):
#     return HttpResponse(json.dumps(captcha()), content_type='application/json')


# 验证验证码
def jarge_captcha(captchaStr, captchaHashkey):
    if captchaStr and captchaHashkey:
        try:
            # 获取根据hashkey获取数据库中的response值
            get_captcha = CaptchaStore.objects.get(hashkey=captchaHashkey)
            if get_captcha.response == captchaStr.lower():  # 如果验证码匹配
                return True
        except:
            return False
    else:
        return False


#   图形验证登陆
class IndexView(View):
    def get(self, request):
        # 判断session是否有用户的名字,没有就退出
        if request.session.get('username', ''):
            return render(request, "index/index.html", {"username": request.session.get('username', ''),
                                                        "com_type": com_type(),
                                                        "hot_li": hot_li,
                                                        "spk_li": spk_li
                                                        })
        hashkey = CaptchaStore.generate_key()  # 验证码答案
        image_url = captcha_image_url(hashkey)  # 验证码地址
        captcha = {'hashkey': hashkey, 'image_url': image_url}
        return render(request, "login.html", locals())

    def post(self, request):
        capt = request.POST.get("captcha", None)  # 用户提交的验证码
        key = request.POST.get("hashkey", None)  # 验证码答案
        if jarge_captcha(capt, key):
            user = request.POST.get("user", None)
            pwd = request.POST.get("pwd", None)
            try:
                # 查询出用户的名字和密码
                user_query = User_info.objects.get(admin=user)
                if user == user_query.admin and pwd == user_query.password:
                    response = render(request, "index/index.html", {"username": user_query.admin,
                                                                    "com_type": com_type(),
                                                                    "hot_li": hot_li,
                                                                    "spk_li": spk_li
                                                                    })
                    # 设置session
                    request.session["username"] = user
                    # 使用json模块设置cookie
                    user = json.dumps(user)
                    response.set_cookie("username", user)
                    return response
            except:
                return HttpResponse("您当前输入用户不存在")
        else:
            return HttpResponse("您当前输入有误")


# 图形验证注册
class ReView(IndexView):
    def get(self, request):
        hashkey = CaptchaStore.generate_key()  # 验证码答案
        image_url = captcha_image_url(hashkey)  # 验证码地址
        captcha = {'hashkey': hashkey, 'image_url': image_url}
        return render(request, "register.html", locals())

    def post(self, request):
        capt = request.POST.get("captcha", None)  # 用户提交的验证码
        key = request.POST.get("hashkey", None)  # 验证码答案
        if jarge_captcha(capt, key):
            user = request.POST.get("user", None)
            pwd = request.POST.get("pwd", None)
            # 查询当前用户是否存在
            admin = User_info.objects.filter(admin=user).all()
            if len(admin) == 0:
                # 创建用户
                User_info.objects.create(
                    admin=user,
                    password=pwd
                )
                return HttpResponse("创建成功，您可以登录了")
            else:
                return self.get(request)
        else:
            return HttpResponse("您当前输入的验证码不正确")


# 导入分页函数
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# 搜索商品方法 and 商品分类方法
def search(request):
    username = ""
    if request.session.has_key("username"):  # 判断session是否存在用户名
        username = request.session.get("username")
    else:
        username = ""
    # 定义queryset 用于区分搜索和选择商品类型
    queryset = None
    search_name = None
    if "search" in request.GET:
        search_name = request.GET.get("search", None)  # 模糊查询
        queryset = Store_Commodity.objects.filter(
            Q(commodity_name__contains=search_name) |  # 使用分页时需使用排序 否则抛出异常
            Q(com_type__type_name=search_name)).all().order_by('id')  # 用q封装，查询商品名或商品类型名
    elif "type" in request.GET:
        search_name = request.GET.get("type", None)
        queryset = Commodity_Type.objects.get(type_name=search_name).store_commodity_set.order_by("id").all()
    page_num = int(request.GET.get("page", "1"))  # 默认为1
    paginator = Paginator(queryset, 10)  # 十条数据为一页
    try:
        # 无异常时返回数据
        page = paginator.page(page_num)
    except PageNotAnInteger:
        # 页数不为整数时返回第一页
        page = paginator.page(1)
    except EmptyPage:
        # 页数不存在时返回结果的最后一页
        page = paginator.page(paginator.num_pages)
    return render(request, "search_page.html", locals())  # 以字典返回全部变量


def change_user(request):
    # 清楚session
    request.session.clear()
    return redirect("/index/login/")


def hello_word(request):

    return render(request, "helloword.html")


# 顶部导航栏的动画
def slideDown(request):
    if request.is_ajax():
        type_name = request.GET.get("type_name", None)
        if type_name:
            # 只要六条数据
            com_query = Commodity_Type.objects.get(type_name=type_name).store_commodity_set.all()[:6]
            com_li = []
            for i in com_query:  # 将query set改造为dict
                idx = {"id": i.id, "commodity": i.commodity_name,
                       "factory": i.factory, "info": i.info,
                       "price": i.price, "img_name": i.img_name,
                       "stock": i.stock, "shop_number": i.shop_number,
                       "click_number": i.click_number, "state": i.state,
                       "com_type_id": i.com_type_id}
                com_li.append(idx)
            return HttpResponse(json.dumps(com_li))
