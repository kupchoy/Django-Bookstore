from django.urls import path
from django.conf.urls import url

from .views import CartPageView, cart_update, purchase, SuccessPageView

urlpatterns = [
    # path('charge/', charge, name='charge'),
    path('', CartPageView.as_view(), name='cart'),
    path('success/', SuccessPageView.as_view(), name='success'),
    url(r'^update/$', cart_update, name='update'),
    url(r'^purchase/$', purchase, name='purchase'),
]