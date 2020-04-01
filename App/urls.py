from App import views
from django.urls import path, re_path

app_name = 'axf01'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('market/', views.market, name='market'),
    path('cart/', views.cart, name='cart'),
    path('mine/', views.mine, name='mine'),
    path('markets/(?P<typeid>\d+/?P<childcid>\d+)/(?P<order_rule>\d+/', views.markets,name='markets'),


    # 注册
    path('register/', views.register, name='register'),
    # 登录
    path('login/', views.login, name='login'),
    # 注册时预检测用户名是否可用
    path('checkuser/', views.check_user, name='check_user'),
    # 注册时预检测用邮箱是否可用
    path('checkemail/', views.check_email, name='check_email'),
    # 退出登录
    path('logout/', views.logout, name='logout'),
    # 激活
    path('activate/', views.activate, name='activate'),
    # 添加商品
    path('addtocart/', views.add_to_cart, name='add_to_cart'),
    # 删除商品
    path('subtocart/', views.sub_to_cart, name='sub_to_cart')


]
