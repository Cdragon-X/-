from django.db import models


# Create your models here.

# 会员表包含
class User_info(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.CharField(max_length=32)    # 用户账号
    password = models.CharField(max_length=64, null=False)  # 密码，不能为空
    username = models.CharField(max_length=64, null=True)   # 真实名，可以为空
    postal_code = models.CharField(max_length=32, null=True)   # 邮政编码，可以为空
    phone = models.CharField(max_length=64, null=True)  # 电话号码，可以为空
    email = models.CharField(max_length=64, null=True)  # 邮编，可以为空
    state = models.CharField(max_length=64, null=True)  # 用户状态，可以为空
    reg_time = models.DateTimeField(auto_now_add=True, null=True)  # 用户注册时间，可以为空


# 购物车表
class Shopping_Cart(models.Model):
    id = models.AutoField(primary_key=True)
    commodity_id = models.IntegerField(null=False)  # 商品id号，不能为空
    commodity_name = models.CharField(max_length=64, null=False)  # 商品名称，不能为空
    price = models.FloatField(max_length=11, null=False)  # 单价，不能为空
    shop_number = models.IntegerField(null=False)    # 购买数量，不能为空
    # 外键关联 与用户表为多对一关系,同时也是会员id
    user_info = models.ForeignKey("User_info", to_field="id", default=1, on_delete=models.CASCADE)


# 订单表包含
class Order(models.Model):
    id = models.AutoField(primary_key=True)
    contacts = models.CharField(max_length=64, null=False)  # 订单联系人，不能为空
    rcv_address = models.CharField(max_length=64, null=False)   # 收货地址，不能为空
    postal_code = models.CharField(max_length=32, null=False)   # 邮政编码，不能为空
    user_phone = models.CharField(max_length=64, null=False)  # 电话号码，不能为空
    shop_time = models.DateTimeField(auto_now_add=True, null=False)  # 购买时间，不能为空
    money = models.FloatField(max_length=11, null=False)  # 总金额，不能为空
    state = models.CharField(max_length=64, null=True)  # 状态，可以为空
    # 外键关联 与用户表为多对一关系,同时也是会员id
    user_info = models.ForeignKey("User_info", to_field="id", default=1, on_delete=models.CASCADE)


# 订单详情表
class Order_Info(models.Model):
    id = models.AutoField(primary_key=True)
    commodity_id = models.IntegerField(null=False)  # 商品id号，不能为空
    commodity_name = models.CharField(max_length=64, null=False)  # 商品名称，不能为空
    price = models.FloatField(max_length=11, null=False)  # 单价，不能为空
    shop_number = models.IntegerField(null=False)    # 购买数量，不能为空
    # 外键关联，与订单表为多对一关系,同时也是订单id号
    order = models.ForeignKey("Order", to_field="id", default=1, on_delete=models.CASCADE)


# 商品类型表
class Commodity_Type(models.Model):
    id = models.AutoField(primary_key=True)
    type_name = models.CharField(max_length=64, null=False)  # 商品类别名，不能为空


# 商品表
class Store_Commodity(models.Model):
    id = models.AutoField(primary_key=True)
    commodity_name = models.CharField(max_length=64, null=False)  # 商品名称，不能为空
    factory = models.CharField(max_length=64, null=False)  # 厂家名称，不能为空
    info = models.CharField(max_length=128, null=False)  # 商品详情，不能为空
    price = models.FloatField(max_length=11, null=False)    # 商品单价，不能为空
    img_name = models.CharField(max_length=64, null=False)  # 图片名称，不能为空
    stock = models.IntegerField(null=False)    # 库存数量，不能为空
    shop_number = models.IntegerField(null=False)    # 购买总数量，不能为空
    click_number = models.IntegerField(null=False)    # 点击总数量，不能为空
    state = models.CharField(max_length=64, null=True)  # 状态，可以为空
    add_time = models.DateTimeField(auto_now_add=True, null=True)  # 添加时间，可以为空
    # 外键关联，与类别为多对一关系，也是商品类别id
    com_type = models.ForeignKey("Commodity_Type", to_field="id", default=1, on_delete=models.CASCADE)


# 所有商品类型
def com_type():
    return Commodity_Type.objects.all()


# 所有热门商品
def hot_com():
    return Store_Commodity.objects.filter(com_type=7).all()[:10]


# 所有音箱
def spk_com():
    return Store_Commodity.objects.filter(com_type=6).all()[:10]