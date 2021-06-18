from django.urls import path,include
from . import views

urlpatterns = [
    #user
    path('', views.index,name = 'user_index'),
    path('update/', views.user_update, name='user_update'),
    path('password/', views.user_password, name='user_password'),
    path('orders/', views.user_order, name='user_orders'),
    path('orderdetail/<int:id>', views.user_orderdetail, name='user_orderdetail'),
    path('orders_product/', views.order_product_detail, name='orders_product'),
    path('comments/', views.user_comments, name='user_comments'),
    path('deletecomment/<int:id>', views.user_deletecomment, name='user_deletecomment'),
]