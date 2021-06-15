from django.urls import path,include
from . import views

urlpatterns = [
    #product
    path('', views.index,name = 'product'),
    path('addcomment/<int:id>', views.addcomment,name = 'addcomment'),
]