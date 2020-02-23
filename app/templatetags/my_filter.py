from django import template
from app.models import Product

register = template.Library()

@register.filter(name='dict_val') 
def dict_val(dic: dict, ind: str):
	return dic[ind]

@register.filter(name='times') 
def times(number):
	return range(number)

@register.filter(name='arind') 
def arind(ar: list, ind: int = 0) -> str:
	a = ar[ind]
	return str(a)

@register.filter(name='obj_cart_name')
def obj_cart_name(obj, ind:int = -1):
	if ind == -1:
		return obj.product.name
	return obj[ind].product.name

@register.filter(name='obj_image')
def obj_image(obj, ind:int = -1):
	if ind == -1:
		return obj.product.all()[0].image.url
	tm = obj[ind]
	return tm.image.url

@register.filter(name='obj_price')
def obj_price(obj, ind:int = -1):
	if ind == -1:
		return obj.product.all()[0].price
	return obj[ind].price

@register.filter(name='obj_slug')
def obj_slug(obj, ind:int = -1):
	if ind == -1:
		return obj.product.all()[0].slug
	return obj[ind].slug

@register.filter(name='obj_cart_count')
def obj_cart_count(obj, ind:int = -1):
	if ind == -1:
		return obj.pr_count
	return obj[ind].pr_count

@register.filter(name='obj_name')
def obj_name(obj, ind:int = -1):
	if ind == -1:
		return obj.product.all()[0].name
	return obj[ind].name

