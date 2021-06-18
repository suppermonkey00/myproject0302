from django.shortcuts import render
from django.http import HttpResponse,HttpRequest,HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages



# Create your views here
from product.models import CommentForm

from product.models import Comment


def index(request):
    return HttpResponse('hello cac ban nho')


def addcomment(request,id):
    url = request.META.get('HTTP_REFERER') # lay Url cuoi cung
    #return HttpResponse(url)
    if request.method == 'POST':  # check post
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()  # tạo mối quan hệ với database
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id=id
            current_user = request.user
            data.user_id = current_user.id
            data.save()  # save data to table
            messages.success(request, "Your review has ben sent. Thank you for your message.")
            return HttpResponseRedirect(url)

    return HttpResponseRedirect(url)