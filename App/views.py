import uuid

from AXF01.settings import MEDIA_KEY_PREFIX
from App.models import MainWheel, MainNav, MainMustBuy, MainShop, MainShow, FoodType, Goods, AXFUser,Cart
from App.views_constant import ALL_TPYE, ORDER_TOTAL, ORDER_PRICE_UP, ORDER_PRICE_DOWN, ORDER_SALE_UP, ORDER_SALE_DOWN, \
    HTTP_USER_EXIST, HTTP_OK
from App.views_heiper import hash_str, send_email_activate
from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse


def home(request):
    main_wheels = MainWheel.objects.all()
    main_navs = MainNav.objects.all()
    main_mustbuys = MainMustBuy.objects.all()
    main_shops = MainShop.objects.all()
    main_shop0_1 = main_shops[0:1]
    main_shop1_3 = main_shops[1:3]
    main_shop3_7 = main_shops[3:7]
    main_shop7_11 = main_shops[7:11]
    main_shows = MainShow.objects.all()
    data = {
        "title": "首页",
        "main_wheels": main_wheels,
        "main_navs": main_navs,
        "main_mustbuys": main_mustbuys,
        "main_shop0_1": main_shop0_1,
        "main_shop1_3": main_shop1_3,
        "main_shop3_7": main_shop3_7,
        "main_shop7_11": main_shop7_11,
        "main_shows": main_shows,
    }
    return render(request, 'main/home.html', context=data)


def market(request):
    return redirect(reverse('axf:markets', kwargs={
        "typeid": 1001,
        "childcid": 0,
        "order_rule": 0,
    }))


def markets(request, typeid, childcid, order_rule):
    foodtypes = FoodType.objects.all()
    goods_list = Goods.objects.filter(categoryid=typeid)

    if childcid == ALL_TPYE:
        pass
    else:
        goods_list = goods_list.filter(childcid=childcid)
    if order_rule == ORDER_TOTAL:
        pass
    elif order_rule == ORDER_PRICE_UP:
        goods_list = goods_list.order_by("price")
    elif order_rule == ORDER_PRICE_DOWN:
        goods_list = goods_list.order_by("-price")
    elif order_rule == ORDER_SALE_UP:
        goods_list = goods_list.order_by("productnum")
    elif order_rule == ORDER_SALE_DOWN:
        goods_list = goods_list.order_by("-productnum")

    foodtype = foodtypes.get(typeid=typeid)
    """
    全部分类：0#进口水果：1001#国产水果：1002

    切割#： [全部分类：0  ，进口水果：1001 ， 国产水果：1002]
    切割：。。。。。
    """
    foodtype_childnames = foodtype.childtypenames
    f_list = foodtype_childnames.split("#")

    f_list_list = []
    for f in f_list:
        f_list_list.append(f.split("："))

    order_rule_list = [
        ['综合排序', ORDER_TOTAL],
        ['价格升序', ORDER_PRICE_UP],
        ['价格降序', ORDER_PRICE_DOWN],
        ['销量升序', ORDER_SALE_UP],
        ['销量降序', ORDER_SALE_DOWN],

    ]
    data = {
        "title": "商城",
        "foodtypes": foodtypes,
        "goods_list": goods_list,
        "typeid": int(typeid),
        "f_list_list": f_list_list,
        "childcid": childcid,
        "order_rule_list": order_rule_list,
        "order_rule_view": order_rule,

    }
    return render(request, 'main/market.html', context=data)


def cart(request):
    return render(request, 'main/cart.html')


def mine(request):
    user_id = request.session.get("user_id")
    data = {
        "title": "我的个人中心",
        "is_login": False,
    }
    if user_id:
        user = AXFUser.objects.get(pk=user_id)
        data["username"] = user.u_name
        if user.u_icon:
            data["icon"] = MEDIA_KEY_PREFIX + user.u_icon.url

        data["is_login"] = True
    return render(request, 'main/mine.html', context=data)


def register(request):
    if request.method == "GET":
        data = {
            "title": "注册"
        }
        return render(request, 'user/register.html', context=data)
    elif request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        icon = request.FILES.get("icon")
        print(request.POST)
        print(password)
        # password=hash_str(password)
        password = make_password(password)
        user = AXFUser()
        user.u_name = username
        user.u_password = password
        user.u_icon = icon
        user.u_email = email
        user.save()
        u_token = uuid.uuid4().hex
        # 缓存过期时间为1天
        cache.set(u_token, user.id, timeout=60 * 60 * 24)
        send_email_activate(username, email, u_token)

        return redirect(reverse("axf:login"))


def login(request):
    if request.method == "GET":
        error_msg = request.session.get('error_msg')
        data = {
            "title": "登录"
        }
        if error_msg:
            # 如果session['error_msg']存在就删除，再传入新的error_msg
            del request.session['error_msg']
            data['error_msg'] = error_msg
        return render(request, 'user/login.html', context=data)

    elif request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        users = AXFUser.objects.filter(u_name=username)

        # exists()方法主要是判断查询的数据是否存在，存在时返回True，否则返回False
        # first() 返回queryset中匹配到的第一个对象，如果没有匹配到对象则为None

        if users.exists():
            user = users.first()
            if check_password(password, user.u_password):
                if user.is_active:

                    request.session['user_id'] = user.id
                    return redirect(reverse('axf:mine'))
                else:
                    request.session['error_msg'] = '未激活'
                    return redirect(reverse('axf:login'))
            else:
                # 密码错误
                request.session['error_msg'] = '密码错误'
                return redirect(reverse('axf:login'))
        # 用户名不存在
        request.session['error_msg'] = '用户不存在'
        return redirect(reverse('axf:login'))


def check_user(request):
    username = request.GET.get("T_name")
    user = AXFUser.objects.filter(u_name=username)
    data = {
        "status": HTTP_OK,
        "msg": 'user can use',
    }
    # exists()判断路径是否存在
    if user.exists():
        data["status"] = HTTP_USER_EXIST
        data["msg"] = 'user already exist'
    else:
        pass
    return JsonResponse(data=data)


def check_email(request):
    email = request.GET.get("T_name")
    e = AXFUser.objects.filter(u_email=email)
    data = {
        "status": HTTP_OK,
        "msg": 'email can use',
    }
    # exists()判断路径是否存在
    if e.exists():
        data["status"] = HTTP_USER_EXIST
        data["msg"] = 'email already exist'
    else:
        pass
    return JsonResponse(data=data)


def logout(request):
    request.session.flush()
    return redirect(reverse("axf:mine"))


def activate(request):
    # 获取从用户点击 激活 传过来的u_token
    u_token = request.GET.get("u_token")
    user_id = cache.get(u_token)

    if user_id:
        # 拿到激活码后就从cache里面把u_token删了，防止用户第二次点击激活
        cache.delete(u_token)
        user = AXFUser.objects.get(pk=user_id)
        user.is_active = True
        user.save()
        return redirect(reverse('axf:login'))

    return render(request, 'user/activate_fail.html')

def add_to_cart(request):
    goodsid = request.GET.get('goodsid')

    # 获取购物车里的数据
    carts = Cart.objects.filter(C_user=request.user).filter(C_goods_id=goodsid)
    print(request.user)
    # 有数据+1
    if carts.exists():
        c_obj = carts.first()
        c_obj.C_goods_num = c_obj.C_goods_num + 1

    # 没有数据创建新的
    else:
        c_obj = Cart()
        c_obj.C_goods_id = goodsid
        c_obj.C_user = request.user

    c_obj.save()

    data = {
        'msg': 1,
        'status': 200,
        "C_goods_num": c_obj.C_goods_num,
    }

    return JsonResponse(data=data)


def sub_to_cart(request):
    goodsid = request.GET.get('goodsid')
    carts = Cart.objects.filter(C_user=request.user).filter(C_goods_id=goodsid)
    data = {
        'msg': 0,
    }
    if carts.exists():
        c_obj = carts.first()
        if c_obj.C_goods_num >= 1:
            c_obj.C_goods_num = c_obj.C_goods_num - 1
            c_obj.save()
            data = {
                'msg': 1,
                'status': 200,
                "C_goods_num": c_obj.C_goods_num,
            }
        if c_obj.C_goods_num == 0:
            Cart.objects.filter(pk=c_obj.id).delete()

    return JsonResponse(data=data)
