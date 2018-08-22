import re
from datetime import datetime
from django.http import HttpResponse, JsonResponse
import json
import datetime
from pip._vendor import requests

from .models import Member, goods, cart, orders, teams, good

########通用方法函数
def addorder(openid, strkey, name1):
    only = name1.get('title') + openid
    newgood = good()
    order1 = orders.objects.get(ordernumber=strkey)
    print(order1)
    newgood.memberid = only
    newgood.Mopid = openid
    newgood.id = name1.get('id')
    newgood.title = name1.get('title')
    newgood.price = name1.get('price')
    newgood.num = name1.get('num')
    newgood.selected = name1.get('selected')
    newgood.orders = order1
    newgood.save()
    print('111111')


def addcart(openid, mopid, now):
    newcart = cart()
    newcart.openid = openid
    newcart.Mopid = mopid
    newcart.date = now
    newcart.save()


def add_member(openid, nickname, strkey):
    newmember = Member()
    newmember.Mopid = openid
    newmember.nickname = nickname
    newmember.invitenumber = strkey
    newmember.Mtotal = 0
    newmember.Mbalance = 0
    newmember.save()


def add_order(ordernumber, nickname, openid, data,money):
    order = orders()
    order.ordernumber = ordernumber
    order.nickname = nickname
    order.openid = openid
    order.date = data
    order.statue = '代发货'
    order.money = money
    order.save()


def decode(key, encrypted_data):  # 传入str 解密调用
    key = str.encode(key)
    encrypted_data = str.encode(encrypted_data)  # 转为bytes形式
    cipher = Fernet(key)
    raw_data = cipher.decrypt(encrypted_data)  # bt
    raw_data = bytes.decode(raw_data)
    return raw_data  # 返回一个str形式的openid，去数据库查询


def addonecart(id, openid, title, num, price, selected):
    only = openid + title
    if good.objects.filter(memberid=only):  # 如果添加过 则更新
        goodone = good()
        goodone.memberid = only
        cart1 = cart.objects.get(openid=openid)
        goodone.id = id
        goodone.Mopid = openid
        goodone2 = good.objects.get(memberid=only)
        goodone.num = goodone2.num + int(num)
        goodone.title = title
        goodone.price = price
        goodone.selected = selected
        goodone.cart = cart1
        goodone.save()
    else:
        cart1 = cart.objects.get(openid=openid)
        goodone = good()
        goodone.memberid = only
        goodone.id = id
        goodone.Mopid = openid
        goodone.num = num
        goodone.title = title
        goodone.price = price
        goodone.selected = selected
        goodone.cart = cart1
        goodone.save()

def AddTeam(openid,Number):
    teamone = teams()
    memberone = Member.objects.get(Mopid=openid)
    teamone.mopid = memberone
    teamone.up = Member.objects.get(invitenumber=Number).Mcardnum2
    teamone.save()
def ChangeTeam(Number,openid):
    memberone = Member.objects.get(invitenumber=Number)
    if not memberone.teams.down1:
        memberone.teams.down1 = Member.objects.get(Mopid=openid).Mcardnum2
        memberone.teams.save()
    elif not memberone.teams.down2:
        memberone.teams.down2 = Member.objects.get(Mopid=openid).Mcardnum2
        memberone.teams.save()
    elif not memberone.teams.down3:
        memberone.teams.down3 = Member.objects.get(Mopid=openid).Mcardnum2
        memberone.teams.save()
    else:
        return HttpResponse('受邀已达上限', content_type='application/json')



##################通用方法


def addAddress(request):
    if request.method == "POST":
        address = request.POST["name"]
        phone = request.POST["phone"]
        detail = request.POST["detail"]
        storage = request.POST["storage"]
        storage = re.findall(r'[\'](.*?)[\']', storage)  # 正则匹配单引号之间的内容，转义
        openid = decode(storage[1], storage[0])
        member = Member.objects.get(Mopid=openid)
        member.Mcardnum2 = address
        member.Mcardnum3 = phone
        member.Mcardnum4 = detail
        member.save()
    return HttpResponse('666', content_type='application/json')


def GetNumber(request):
    if request.method == "POST":
        storage = request.POST["storage"]
        storage = re.findall(r'[\'](.*?)[\']', storage)
        openid = decode(storage[1], storage[0])
        memberone = Member.objects.get(Mopid=openid)
        number = memberone.invitenumber
    return HttpResponse(number, content_type='application/json')

def CheckNumber(request):
    if request.method == "POST":
        storage = request.POST["storage"]
        storage = re.findall(r'[\'](.*?)[\']', storage)
        openid = decode(storage[1], storage[0])
        Number = request.POST["Number"]
        if  Member.objects.filter(Mopid=openid).exists(): #判断该用户是否建立
            if  Member.objects.filter(invitenumber=Number): #判断邀请码是否有效
                if Member.objects.get(invitenumber=Number).Mopid == Member.objects.get(Mopid=openid).Mopid:
                    return HttpResponse('不能自己使用', content_type='application/json')
                else:
                    AddTeam(openid,Number)
                    ChangeTeam(Number,openid)
            else:
                return HttpResponse('邀请码无效', content_type='application/json')
        else:
            return HttpResponse('用户不存在', content_type='application/json')
    return HttpResponse('加入成功', content_type='application/json')

def OpenTeam (request):
    if request.method == "POST":
        storage = request.POST["storage"]
        storage = re.findall(r'[\'](.*?)[\']', storage)
        openid = decode(storage[1], storage[0])
        if Member.objects.get(Mopid=openid).teams :
            return HttpResponse('1', content_type='application/json')
        else:
            return HttpResponse('0', content_type='application/json')




def AddtoOrder(request):  # 等到支付完成后再加入订单中
    key = Fernet.generate_key()  # bt 每次都随机生成 所以要传给前端
    strkey = bytes.decode(key)  # 随机生成的订单号
    print(strkey)
    global data, List, Testcard
    now = datetime.datetime.now()
    print('=======', now)
    if request.method == "POST":
        Name = request.POST["cart"]  # str
        name1 = json.loads(Name)  # list
        print('11111', name1)
        nickname = request.POST["nickname"]
        storage = request.POST["storage"]
        money = request.POST["money"]
        storage = re.findall(r'[\'](.*?)[\']', storage)  # 正则匹配单引号之间的内容，转义
        openid = decode(storage[1], storage[0])
        add_order(strkey, nickname, openid, now,money)# 此处已修改 前端应该加入money参数
        for key in name1:  # name1为list.
            addorder(openid, strkey, key)
    return HttpResponse(strkey, content_type='application/json')


def oneAddToCart(request):
    now = datetime.datetime.now()
    if request.method == "POST":
        id = request.POST["id"]
        title = request.POST["title"]
        image = request.POST["image"]
        num = request.POST["num"]
        price = request.POST["price"]
        selected = True
        mopid = request.POST["nickname"]
        storage = request.POST["storage"]
        storage = re.findall(r'[\'](.*?)[\']', storage)  # 正则匹配单引号之间的内容，转义
        openid = decode(storage[1], storage[0])
        cartone = cart.objects.filter(openid=openid)
        if len(cartone) > 0:  # 判断用户是否有购物车
            cartone.date = now
            cartone.mopid = mopid
            addonecart(id, openid, title, num, price, selected)
        else:
            addcart(openid, mopid, now)
            addonecart(id, openid, title, num, price, selected)
    return HttpResponse('666', content_type='application/json')


def oneToGood(request):
    if request.method == "POST":
        id = request.POST["id"]
        goodsone = goods.objects.filter(id=id).values('id', 'image', 'title', 'price', 'stock', 'detail', 'parameter',
                                                      'service')
        good = list(goodsone)
        goodsone = json.dumps(good)
        print(goodsone, type(goodsone))
    return HttpResponse(goodsone, content_type='application/json')


def getcart(request):
    if request.method == "POST":
        storage = request.POST["storage"]
        storage = re.findall(r'[\'](.*?)[\']', storage)  # 正则匹配单引号之间的内容，转义
        openid = decode(storage[1], storage[0])
        ret = good.objects.filter(cart=cart.objects.get(openid=openid)).values('id', 'title', 'price', 'num',
                                                                               'selected')  # 转化为dict形式的queryset
        # goods = json.dumps(good1)
        rets = list(ret)
        goods = json.dumps(rets)
        # goods = serializers.serialize("json", ret)
    return HttpResponse(goods, content_type='application/json')
    # return render(request, 'test.html')


def getorder(request):
    if request.method == "POST":
        ordernumber = request.POST["ordernumber"]
        ret = good.objects.filter(orders=orders.objects.get(ordernumber=ordernumber)).values('id', 'title', 'price',
                                                                                             'num',
                                                                                             'selected')  # 转化为dict形式的queryset
        rets = list(ret)
        goods = json.dumps(rets)
    return HttpResponse(goods, content_type='application/json')


from cryptography.fernet import Fernet  # 加密


def get_id(request):
    if request.method == "POST":
        code = request.POST["code"]
        nickname = request.POST["nickname"]
        appid = 'wx8afb82a4691cff58'
        secret = '570073721c05350cf4cd86b02348ebe1'
        api = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + appid + '&secret=' + secret + '&js_code=' + code + '&grant_type=authorization_code'
        res = requests.get(api)
        # content = res.content #bytes
        # text = res.text #str
        json_data = res.json()  # dict
        print(json_data.get('openid'))
        openid = json_data.get('openid')
        key = Fernet.generate_key()  # bt 每次都随机生成 所以要传给前端
        strkey = bytes.decode(key)
        cipher = Fernet(key)  # bt
        encrypted_data = cipher.encrypt(openid.encode('utf-8'))  # bt
        strencrypted_data = bytes.decode(encrypted_data)  # 加密后的openid-str
        # dic = {'encrypted_data': encrypted_data, 'strkey': strkey, }
        dic = ([encrypted_data], [strkey])  # list
        print(dic)
        member = Member.objects.filter(Mopid=openid)
        if len(member) == 0:
            now = datetime.datetime.now()
            add_member(openid, nickname, strkey)
            addcart(openid, nickname, now)
            # add_order(strkey, nickname, openid, now)
    return HttpResponse(dic, content_type='application/json')  # 传给前端的str形式的openid和key
