"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path,include

import home
from home import views
from order import views as OrderViews
from user import views as Userviews




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('product/',include('product.urls')),
    path('home', include('home.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')), #ckeditor
    path('order/', include('order.urls')),
    path('user/', include('user.urls'),name = 'user'),

    path('about/',views.aboutus,name = 'aboutus'),
    path('search/', views.search, name='search'),
    path('search_auto/', views.search_auto, name='search_auto'),
    path('contact/',views.contactus,name = 'contactus'),
    path('category/<int:id>/<slug:slug>', views.category_products, name='category_products'),
    path('product/<int:id>/<slug:slug>', views.product_detail, name='product_detail'),
    path('shopcart/', OrderViews.shopcart, name='shopcart'),
    path('login/', Userviews.login_form, name='login_form'),
    path('signup/', Userviews.signup_form, name='signup_form'),
    path('logout/', Userviews.logout_form, name='logout_form'),
    path('faq/', views.faq, name='faq'),
    path('ajaxcolor/', views.ajaxcolor, name='ajaxcolor'),

]
if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
