from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Product, Account, Article, Pr_class, Sub_Pr_class, Cart, Order

class MembershipInline(admin.TabularInline):
	model = Cart
	extra = 0

@admin.register(Pr_class)
class Pr_classAdmin(admin.ModelAdmin):
	list_display = ('id', 'name')

@admin.register(Sub_Pr_class)
class Sub_Pr_classAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'main_pr_class')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'sub_product_class', 'price')


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'password')
	inlines = (MembershipInline,)

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
	list_display = ('id', 'name',)
	filter_horizontal = ('product',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
	pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	pass