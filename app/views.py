from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.core.paginator import Paginator
from urllib.parse import urlparse
from .models import Product, Pr_class, Sub_Pr_class, Account, Cart,  Article, Order
from .forms import RegisterForm, AuthorisationForm, HiddenCartForm

def category(request):
	pr_class_objects =  Pr_class.objects.all()
	sub_pr_class_objects_dict = {}

	for obj in pr_class_objects:
		sub_pr_class_objects = Sub_Pr_class.objects.all().filter(main_pr_class=obj)
		sub_pr_class_objects_dict[obj.name] = sub_pr_class_objects

	return {
		'class_obj': pr_class_objects,
		'sub_pr_class_objects_dict': sub_pr_class_objects_dict
	}


def index(request):
	template = 'index.html'

	my_request = request.GET.get('sort')
	need_replace = (str(my_request).find(' ',0,len(str(my_request))))!=-1
	request_list = str(my_request).replace('/', '')
	request_list = request_list.replace('_', ' ').split()
	if need_replace:
		request_list[1] = request_list[1]+' '+request_list[2]
		del request_list[2]
	orderBy = False

	current_page = 1
	if request_list!=['None'] and request_list[2]!='1':
		current_page = int(request_list[2])

	if request_list!=['None'] and request_list[0]!='none':
		if request_list[0]=='name':
			orderBy = 'product__name'
			first_href_part = '?sort=name_'
		elif request_list[0]=='minPrice':
			orderBy = 'product__price'
			first_href_part = '?sort=minPrice_'
		elif request_list[0]=='maxPrice':
			orderBy = '-product__price'
			first_href_part = '?sort=maxPrice_'
		else:
			first_href_part = '?sort=none_'
	else:
		first_href_part = '?sort=none_'


	if request_list!=['None'] and request_list[1]!='none' and str(request_list[1])!='None':
		class_str = request_list[1] 

		if class_str[0]=='^':
			class_str = class_str[1:]
			class_obj = Sub_Pr_class.objects.get(name=class_str)
			if orderBy:
				objects = Article.objects.all().filter(product__sub_product_class=class_obj).order_by(orderBy)
			else:
				objects = Article.objects.all().filter(product__sub_product_class=class_obj)

		else:
			class_obj = Pr_class.objects.get(name=request_list[1])
			sub_class_obj_list = Sub_Pr_class.objects.all().filter(main_pr_class=class_obj)
			if orderBy:
				objects = Article.objects.all().filter(product__sub_product_class__in=sub_class_obj_list).order_by(orderBy)
			else:
				objects = Article.objects.all().filter(product__sub_product_class__in=sub_class_obj_list)

		second_href_part = '_' + request_list[1] + '_'

	else:
		if orderBy:
			objects = Article.objects.all().order_by(orderBy)
		else:
			objects = Article.objects.all()
		second_href_part = '_none_'


	if objects.exists():
		have_objects = True
		paginator = Paginator(objects, 3)
		page = paginator.get_page(current_page)
		datalist = page.object_list

		if page.has_next():
			next_page_url = first_href_part + second_href_part + str(page.next_page_number())
			if (request_list!=['None'] and request_list[2]!='1'): current_page = page.next_page_number()-1
		else:
			next_page_url = None
		
		if page.has_previous():
			previous_page_url = first_href_part + second_href_part + str(page.previous_page_number())
			if (request_list!=['None'] and request_list[2]!='1'): current_page = page.previous_page_number()+1
		else:
			previous_page_url = None

		object_count = datalist.count()
	else:
		have_objects = False
		next_page_url = None
		previous_page_url = None
		object_count = 0
		datalist = None

	is_guest = True
	if 'acc' in request.session.keys() and request.session['acc'] != 'гость': 
		is_guest = False

	hid_form = HiddenCartForm()
	if request.method == 'POST':
		if not is_guest:
			acc = Account.objects.get(name=request.session['acc'])
			hid_form = HiddenCartForm(request.POST)

			if hid_form.is_valid():
				name = hid_form.clean_name()
				print('----------------------')
				print(name)
				print('----------------------')
				product = Product.objects.get(name=name)

				if Cart.objects.all().filter(account=acc, product=product).exists():
					cart = Cart.objects.get(account=acc, product=product)
					Cart.objects.all().filter(account=acc, product=product).update(pr_count=cart.pr_count + 1)
				else:
					new_cart = Cart(account=acc, product=product, pr_count=1)
					new_cart.save()


	context = {
	'objects': datalist,
	'ides': [i for i in range(object_count)],
	'href_name': '/?sort=name'+second_href_part+str(current_page),
	'href_min_price': '/?sort=minPrice'+second_href_part+str(current_page),
	'href_max_price': '/?sort=maxPrice'+second_href_part+str(current_page),
	'first_href_part': first_href_part,
	'prev_page_url':previous_page_url,
	'next_page_url':next_page_url,
	'current_page':'_'+str(current_page),
	'is_guest': is_guest,
	'form': hid_form,
	'have_objects': have_objects
	}

	return render(request, template, context)


def login_home(request):
	template = 'login_home.html'

	is_guest = False
	acc = request.session.get('acc', 'гость')

	if 'acc' not in request.session.keys():
		request.session['acc'] = 'гость'
		is_guest = True

	elif request.session['acc'] == 'гость':
		is_guest = True

	context = {
		'acc': request.session['acc'],
		'is_guest': is_guest
	}

	return render(request, template, context)


def signup(request):
	template = 'signup.html'

	error = 'Заполните пожалуйста данные поля'
	no_error = True

	if request.method == 'POST':
		registration_form = RegisterForm(request.POST)

		if registration_form.is_valid():
			name = registration_form.clean_name()
			password = registration_form.clean_password()
			password_again = registration_form.clean_password_again()

			if password != password_again:
				error = 'Пароли не совпадают'
				no_error = False
			else:
				try:
					obj = Account.objects.get(name=name)
					error = 'Аккаунт с таким адресом электронной почты уже существует'
					no_error = False
				except:
					pass
				if name == 'гость':
					error = 'Пароли не совпадают'
					no_error = False

			if no_error:
				request.session['acc'] = name
				new_acc = Account(name=name, password=password)
				new_acc.save()
				return redirect('/home_of_login/')

	else:
		registration_form = RegisterForm()

	context = {
		'registration_form': registration_form,
		'error': error
	}

	return render(request, template, context)

def login(request):
	template = 'login.html'

	no_error = True
	error = 'Заполните пожалуйста данные поля'

	if request.method == 'POST':
		authorisation_form = AuthorisationForm(request.POST)

		if authorisation_form.is_valid():
			name = authorisation_form.clean_name()
			password = authorisation_form.clean_password()

			try:
				obj = Account.objects.get(name=name)
				if password != obj.password:
					no_error = False
					error = 'Адрес электронной почты или пароль неверный'
			except:
				no_error = False
				error = 'Адрес электронной почты пользователя или пароль неверный'

			if no_error:
				request.session['acc'] = name
				return redirect('/home_of_login/')

	else:
		authorisation_form = AuthorisationForm()

	context = {
		'authorisation_form': authorisation_form,
		'error': error
	}

	return render(request, template, context)

def logout(request):
	template = 'logout.html'
	
	request.session['acc'] = 'гость'

	context = {}

	return render(request, template, context)

def cart_view(request):
	template = 'cart.html'

	no_product = True
	if 'acc' in request.session.keys() and request.session['acc'] != 'гость': 
		user_acc = Account.objects.get(name=request.session['acc'])
		obj_cart = Cart.objects.all().filter(account=user_acc)
		obj_count_int = obj_cart.count()
		is_guest = False
		name = request.session['acc']

		if obj_cart.exists():
			no_product = False

	else:
		obj_cart = None
		is_guest = True
		name = None
		obj_count_int = None

	context = {
		'objects': obj_cart,
		'name': name,
		'is_guest':is_guest,
		'obj_count_int': obj_count_int,
		'no_product':no_product
	}

	return render(request, template, context)


def product_view(request, slug):
	template = 'product_detail.html'

	product = get_object_or_404(Product, slug=slug)

	is_guest = True
	if 'acc' in request.session.keys() and request.session['acc'] != 'гость': 
		is_guest = False

	if request.method == 'POST':
		if not is_guest:
			acc = Account.objects.get(name=request.session['acc'])

			if Cart.objects.all().filter(account=acc, product=product).exists():
				cart = Cart.objects.get(account=acc, product=product)
				Cart.objects.all().filter(account=acc, product=product).update(pr_count=cart.pr_count + 1)
			else:
				new_cart = Cart(account=acc, product=product, pr_count=1)
				new_cart.save()

	context = {
		'product':product,
		'is_guest':is_guest
	}

	return render(request, template, context)

def clean_cart(request):
	template = 'cart_delete.html'

	if 'acc' in request.session.keys() and request.session['acc'] != 'гость': 
		is_guest = False
		acc = Account.objects.get(name=request.session['acc'])
		cart_objects = Cart.objects.all().filter(account=acc)
		for obj in cart_objects:
			order = Order(account=obj.account, product=obj.product, pr_count=obj.pr_count)
			order.save()
		Cart.objects.all().filter(account=acc).delete()
	else:
		is_guest = True

	context = {
		'is_guest': is_guest
	}

	return render(request, template, context)