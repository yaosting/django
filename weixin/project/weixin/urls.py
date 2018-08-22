from  django.conf.urls import url
from django.views.generic import RedirectView
from . import  views

urlpatterns = [
url(r'^test/$', views.AddtoOrder ),
url(r'^test1/$', views.getcart ),
url(r'^get_order/$', views.getorder ),
url(r'^addAddress/$', views.addAddress ),
url(r'^GetNumber/$', views.GetNumber ),
url(r'^CheckNumber/$', views.CheckNumber ),
url(r'^OpenTeam/$', views.OpenTeam ),

url(r'^getid/$', views.get_id ),
url(r'^oneAddToCart/$', views.oneAddToCart ),
url(r'^oneToGood/$', views.oneToGood ),

]