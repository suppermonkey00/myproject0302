from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader



# Create your views here
from home.models import Setting

from home.models import ContactForm

from home.models import ContactMessage

from product.models import Category

from product.models import Product

from home.forms import SearchForm

import json

from product.models import Images

from product.models import Comment

from home.models import FAQ

from product.models import Variants


def index(request):
    setting =Setting.objects.get(pk=1)
    page = 'home'
    products_slider=Product.objects.all().order_by('id')[:4]    #4 san pham dau
    products_latest = Product.objects.all().order_by('-id')[:4] #4 san pham cuoi
    products_picked = Product.objects.all().order_by('?')[:4]   #4 san pham random
    category = Category.objects.all()
    context = {'setting':setting,
               'page':page,
               'products_slider': products_slider,
               'products_latest': products_latest,
               'products_picked': products_picked,
               'category':category,}
    return render(request, 'index.html',context)

def aboutus(request):
    category = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting,'category':category}
    return render(request, 'about.html',context)

def contactus(request):
    if request.method == 'POST':  # check post
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()  # tạo mối quan hệ với database
            data.name = form.cleaned_data['name']  # get form input data
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()  # save data to table
            messages.success(request, "Your message has ben sent. Thank you for your message.")
            return HttpResponseRedirect('/contact')
    setting = Setting.objects.get(pk=1)
    form = ContactForm
    category = Category.objects.all()
    context = {'setting': setting,'form':form,'category':category}
    return render(request, 'contatctus.html', context)


def category_products(request,id,slug):
    category = Category.objects.all()
    #products = Product.objects.filter(category_id=id)
    products = Product.objects.filter(category_id=id)
    # Paging
    paginator = Paginator(products, 3)
    page = request.GET.get('page', 1)
    try:
        orders_paged = paginator.page(page)
    except PageNotAnInteger:
        orders_paged = paginator.page(1)
    except EmptyPage:
        orders_paged = paginator.page(paginator.num_pages)

    context = {'products': products,
               'category': category,
               "orders": orders_paged,
               }
    return render(request, 'category_products.html', context)


def search(request):
    if request.method == 'POST':  # check post
        form = SearchForm(request.POST) #kiem tra form
        if form.is_valid():
            query=form.cleaned_data['query']
            catid=form.cleaned_data['catid']
            if catid==0:
                products=Product.objects.filter(title__icontains=query) # lua chon * loc tu product tim kiem tu khoa "query"
            else:
                products=Product.objects.filter(title__icontains=query,category_id=catid)
            category=Category.objects.all()
            context = {
                        'products':products,
                        'query':query,
                        'category':category,
            }
        return render(request, 'search_products.html',context)
    return HttpResponseRedirect('/')

def search_auto(request): #http://lalicode.com/post/5/ search_auto
  if request.is_ajax():
    q = request.GET.get('term', '')
    products = Product.objects.filter(title__icontains=q)
    results = []
    for rs in products:
      products_json = {}
      products_json = rs.title
      results.append(products_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)

def product_detail(request,id,slug):
    query = request.GET.get('q')
    category = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status= 'True')
    context = {'product': product,
               'category': category,
               'images': images,
               'comments': comments,
               }
    if product.variant !="None": # Product have variants
        if request.method == 'POST': #if we select color
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id) #selected product by click color radio
            colors = Variants.objects.filter(product_id=id,size_id=variant.size_id )
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
            query += variant.title+' Size:' +str(variant.size) +' Color:' +str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id,size_id=variants[0].size_id )
            sizes = Variants.objects.raw('SELECT * FROM  product_variants  WHERE product_id=%s GROUP BY size_id',[id])
            variant =Variants.objects.get(id=variants[0].id)
        context.update({'sizes': sizes, 'colors': colors,
                        'variant': variant,'query': query
                        })
    return render(request,'product_detail.html',context)


def ajaxcolor(request):
    data = {}
    if request.POST.get('action') == 'post':
        size_id = request.POST.get('size')
        productid = request.POST.get('productid')
        colors = Variants.objects.filter(product_id=productid, size_id=size_id)
        context = {
            'size_id': size_id,
            'productid': productid,
            'colors': colors,
        }
        data = {'rendered_table': render_to_string('color_list.html', context=context)}
        return JsonResponse(data)
    return JsonResponse(data)

def faq(request):
    category = Category.objects.all()
    faq = FAQ.objects.filter(status = 'True').order_by('ordernumber')
    context = {'faq': faq, 'category': category}
    return render(request, 'faq.html', context)



