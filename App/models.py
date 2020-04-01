from django.db import models


class Main(models.Model):
    img = models.CharField(max_length=255)
    name = models.CharField(max_length=64)
    trackid = models.IntegerField(default=1)

    class meta:
        abstract = True


class MainWheel(Main):
    class Meta:
        db_table = 'axf_wheel'


class MainNav(Main):
    class Meta:
        db_table = 'axf_nav'


class MainMustBuy(Main):
    class Meta:
        db_table = 'axf_mustbuy'


class MainShop(Main):
    class Meta:
        db_table = 'axf_shop'


class MainShow(Main):
    # 分类的id
    categoryid = models.IntegerField(default=1)
    # 名称
    brandname = models.CharField(max_length=64)
    # 图片
    img1 = models.CharField(max_length=255)
    # 分类
    childcid1 = models.IntegerField(default=1)
    # 商品编码
    productid1 = models.IntegerField(default=1)
    # 长名字
    longname1 = models.CharField(max_length=128)
    # 价格
    price1 = models.FloatField(default=1)
    # 超市价格
    marketprice1 = models.FloatField(default=0)

    img2 = models.CharField(max_length=255)
    childcid2 = models.IntegerField(default=1)
    productid2 = models.IntegerField(default=1)
    longname2 = models.CharField(max_length=128)
    price2 = models.FloatField(default=1)
    marketprice2 = models.FloatField(default=0)

    img3 = models.CharField(max_length=255)
    childcid3 = models.IntegerField(default=1)
    productid3 = models.IntegerField(default=1)
    longname3 = models.CharField(max_length=128)
    price3 = models.FloatField(default=1)
    marketprice3 = models.FloatField(default=0)

    class Meta:
        db_table = 'axf_mainshow'


class FoodType(models.Model):
    typeid = models.IntegerField(default=1)
    typenames = models.CharField(max_length=32)
    childtypenames = models.CharField(max_length=255)
    typesort = models.IntegerField(default=1)

    class meta:
        db_table = 'axf_foodtype'


class Goods(models.Model):
    productid = models.IntegerField(default=1)
    productimg = models.CharField(max_length=255)
    productname = models.CharField(max_length=128)
    productlongname = models.CharField(max_length=255)
    isxf = models.BooleanField(default=False)
    esc = models.BooleanField(default=False)
    isc = models.CharField(max_length=64)
    price = models.FloatField(default=0)
    marketprice = models.FloatField(default=1)
    categoryid = models.IntegerField(default=1)
    childcid = models.IntegerField(default=1)
    childcidname = models.CharField(max_length=128)
    dealerid = models.IntegerField(default=1)
    storenums = models.IntegerField(default=1)
    productnum = models.IntegerField(default=1)

    class meta:
        db_table = 'axf_goods'


class AXFUser(models.Model):
    u_name = models.CharField(max_length=32, unique=True)
    u_password = models.CharField(max_length=256)
    u_email = models.CharField(max_length=64, unique=True)
    u_icon = models.ImageField(upload_to='icons/%Y/%m/%d/')
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    class Meta:
        db_table = 'axf_user'

# 购物车
class Cart(models.Model):
    # Foreign Key外键,on_delete=models.CASCADE此值设置，是级联删除,django2必须加这一项
    C_user = models.ForeignKey(AXFUser,on_delete=models.CASCADE)
    C_goods = models.ForeignKey(Goods,on_delete=models.CASCADE)

    C_goods_num = models.IntegerField(default=1)
    C_is_select = models.BooleanField(default=True)

    class Meta:
        db_table = 'axf_cart'
