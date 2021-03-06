from django.shortcuts import render
from django.http import HttpResponse,HttpRequest,HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm




# Create your views here.
from product.models import Category

from user.models import UserProfile

from user.forms import SignUpForm

from user.forms import UserUpdateForm

from user.forms import ProfileUpdateForm

from order.models import Order

from order.models import OrderProduct

from product.models import Comment


@login_required(login_url = '/login') #check login
def index(request):
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    category = Category.objects.all()
    context = {
        'category': category,
        'profile': profile,
    }
    return render(request, 'user_profile.html', context)


def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            current_user = request.user
            userprofile = UserProfile.objects.get(user_id=current_user.id)
            request.session['userimage'] = userprofile.image.url
            # Redirect to a success page.
            return HttpResponseRedirect('/')
        else:
            # Return an 'invalid login' error message.
            messages.warning(request,'login error! tai khoan hoac mat khau khong dung')
            HttpResponseRedirect('/login')
    category = Category.objects.all()
    context = {
        'category':category,
    }
    return render(request,'login_form.html',context)


def logout_form(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect('/')


def signup_form(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username= form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id=current_user.id
            data.image="images/users/user.png"
            data.save()
            messages.success(request, 'Your account has been created!')
            return HttpResponseRedirect('/')
        else:
            messages.warning(request,form.errors)
            return HttpResponseRedirect('/signup')


    form = SignUpForm()
    category = Category.objects.all()
    context = {
        'category': category,
        'form': form,
    }
    return render(request, 'signup_form.html', context)


@login_required(login_url='/login') # Check login
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user) # request.user is user  data
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return HttpResponseRedirect('/user')
    else:
        category = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile) #"userprofile" model -> OneToOneField relatinon with user
        context = {
            'category': category,
            'user_form': user_form,
            'profile_form': profile_form
        }
        return render(request, 'user_update.html', context)


@login_required(login_url='/login') # Check login
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request,'ban da thay doi password thanh cong')
            return HttpResponseRedirect('/user')
        else:
            messages.error(request,form.errors)
            return HttpResponseRedirect('/user/password')
    else:
        category = Category.objects.all()
        form = PasswordChangeForm(request.user)
        context = {
            'category': category,
            'form': form,
        }
        return render(request, 'user_password.html', context)



@login_required(login_url='/login') # Check login
def user_order(request):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.filter(user_id = current_user.id)
    context = {
        'category': category,
        'order': order,
    }
    return render(request, 'user_order.html', context)



@login_required(login_url='/login') # Check login
def user_orderdetail(request, id):
    category = Category.objects.all()
    current_user = request.user
    order = Order.objects.get(user_id=current_user.id, id=id)
    orderitems = OrderProduct.objects.filter(order_id = id)
    context = {
        'category': category,
        'order': order,
        'orderitems': orderitems,
    }
    return render(request, 'user_order_detail.html', context)


@login_required(login_url='/login') # Check login
def order_product_detail(request):
    category = Category.objects.all()
    current_user = request.user
    order_product = OrderProduct.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'order_product': order_product,
    }
    return render(request, 'user_order_products.html', context)

@login_required(login_url='/login') # Check login
def user_comments(request):
    category = Category.objects.all()
    current_user = request.user
    comments = Comment.objects.filter(user_id=current_user.id)
    context = {
        'category': category,
        'comments': comments,
    }
    return render(request, 'user_comments.html', context)


@login_required(login_url='/login') # Check login
def user_deletecomment(request,id):
    current_user = request.user
    Comment.objects.filter(id=id,user_id = current_user.id).delete()
    messages.success(request, 'ban da xoa san pham khoi gio hang')
    return HttpResponseRedirect('/user/comments')