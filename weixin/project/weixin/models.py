from django.db import models


class Member(models.Model):
    Mopid = models.CharField('用户openid', primary_key=True, max_length=50)
    session_key = models.CharField('session_key', max_length=50, null=True, blank=True)
    Mcardnum2 = models.CharField('姓名', max_length=50, null=True, blank=True)
    Mcardnum3 = models.CharField('手机号', max_length=50, null=True, blank=True)
    Mcardnum4 = models.CharField('收货地址', max_length=50, null=True, blank=True)
    invitenumber = models.CharField('邀请码', max_length=50, null=True, blank=True)
    nickname = models.CharField('昵称', max_length=50)  # 持卡人姓名
    Mtotal = models.CharField('累计消费', max_length=50, null=True, blank=True)  # 累计消费
    Mbalance = models.DecimalField('我的钱包', max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = '用户信息'


class goods(models.Model):
    id = models.CharField('商品编号', max_length=10, primary_key=True, )
    image = models.CharField('图片路径', max_length=50)
    title = models.CharField('商品名称', max_length=10)  # 商品名称
    price = models.CharField('商品售价', max_length=10)  # 商品售价
    stock = models.CharField('有/无货', max_length=10)
    detail = models.CharField('详情', max_length=10)
    parameter = models.CharField('商品规格', max_length=10)
    service = models.CharField('售后说明', max_length=10)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '商品信息'


class cart(models.Model):
    Mopid = models.CharField('用户昵称', max_length=50)
    openid = models.CharField('用户openid', primary_key=True, max_length=50)
    date = models.DateField('日期', )  # 日期

    def __str__(self):
        return self.Mopid

    class Meta:
        verbose_name = '用户购物车'


class orders(models.Model):
    ordernumber = models.CharField('用户订单号', primary_key=True, max_length=50)
    nickname = models.CharField('用户昵称', max_length=50)
    openid = models.CharField('用户openid', max_length=50)
    statue  = models.CharField('订单状态', max_length=10,default='待发货')
    money = models.CharField('总金额', max_length=10)
    date = models.DateField('日期', )  # 日期

    def __str__(self):
        return self.ordernumber

    class Meta:
        verbose_name = '用户订单'


class teams(models.Model):
    mopid = models.OneToOneField(Member, on_delete=models.CASCADE, primary_key=True, )
    up = models.CharField('up', max_length=50, null=True, blank=True)
    down1 = models.CharField('down1', max_length=50, null=True, blank=True)
    down2 = models.CharField('down2', max_length=50, null=True, blank=True)
    down3 = models.CharField('down3', max_length=50, null=True, blank=True)

    def __str__(self):
        return 'carts:{}'.format(self.mopid.Mopid, self.mopid.nickname)

    class Meta:
        verbose_name = '团队信息'


class good(models.Model):
    memberid = models.CharField('唯一标识', max_length=100, primary_key=True, )
    Mopid = models.CharField('用户openid', max_length=50)
    id = models.CharField('商品编号', max_length=10, )
    title = models.CharField('商品名称', max_length=10)
    price = models.CharField('商品售价', max_length=10)
    num = models.IntegerField('商品数量', null=True, blank=True)
    selected = models.BooleanField('是否勾选', default=False)
    cart = models.ForeignKey("cart", null=True, blank=True, on_delete=models.CASCADE, )
    orders = models.ForeignKey("orders", null=True, blank=True, on_delete=models.CASCADE, )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '商品'
