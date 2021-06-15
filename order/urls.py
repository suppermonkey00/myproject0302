from django.urls import path,include
from . import views

urlpatterns = [
    #product
    path('', views.index,name = 'order'),
    path('addtoshopcart/<int:id>', views.addtoshopcart, name='addtoshopcart'),
    path('deletefromcart/<int:id>', views.deletefromcart, name='deletefromcart'),
    path('orderproduct', views.orderproduct, name='orderproduct'),

]