from django.contrib import admin

# Register your models here.
from .models import Member,goods,cart,orders,teams,good

class goodInfo(admin.TabularInline):
    model = good
    extra = 2
class cartAdmin(admin.ModelAdmin):
    inlines = [goodInfo]
    # 列表页属性
    list_display = ['Mopid','date','openid']  #显示字段
    list_per_page = 5  #分页
    search_fields = ['openid']  #搜索字段
    fieldsets = [
        ("head", {"fields": [ 'Mopid','date','openid']}),

    ] #分组显示
    # 执行动作位置
    actions_on_top = False
    actions_on_bottom = True


class ordersAdmin(admin.ModelAdmin):
    inlines = [goodInfo]
    # 列表页属性
    list_display = ['ordernumber','nickname','openid','date']  #显示字段
    list_per_page = 3  #分页
    search_fields = ['openid']  #搜索字段
    # 添加，修改页属性
    # fields = []
    fieldsets = [
        ("head", {"fields": ['ordernumber','nickname','openid','date']}),

    ] #分组显示
    # 执行动作位置
    actions_on_top = False
    actions_on_bottom = True


admin.site.register(goods,)
admin.site.register(cart,cartAdmin)
admin.site.register(Member,)
admin.site.register(orders,ordersAdmin)
admin.site.register(teams)
admin.site.register(good)