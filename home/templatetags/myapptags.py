from django import template

from mysite import settings
from order.models import ShopCart

register = template.Library()

@register.simple_tag
def shopcartcount(userid):
    count = ShopCart.objects.filter(user_id=userid).count()
    return count