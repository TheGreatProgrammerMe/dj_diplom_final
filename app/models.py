from django.db import models


class Pr_class(models.Model):
	name = models.CharField(max_length=256)

	def __str__(self):
		return self.name

class Sub_Pr_class(models.Model):
	name = models.CharField(max_length=256)
	main_pr_class = models.ForeignKey(Pr_class, on_delete = models.CASCADE)

	def __str__(self):
		return self.name


class Product(models.Model):
	name = models.CharField(max_length=256, verbose_name='название продукта')
	image = models.FileField(upload_to='products/%Y/%m/%d/')
	slug = models.SlugField()
	sub_product_class = models.ForeignKey(Sub_Pr_class, on_delete = models.CASCADE, verbose_name='подкласс продукта')
	description = models.CharField(max_length=1024, verbose_name='описание продукта', default='-')
	price = models.DecimalField(
    	max_digits = 7,
    	decimal_places = 2
    )


	def __str__(self):
		return self.name

class Account(models.Model):
	name = models.EmailField(verbose_name='адрес электронной почты пользователя')
	password = models.CharField(max_length=256, verbose_name='пароль')
	products = models.ManyToManyField(
		Product, 
    	blank=True, 
    	through="Cart"
    	)

	def __str__(self):
		return self.name


class Article(models.Model):
	name = models.CharField(max_length=256, verbose_name='название статьи')
	text = models.TextField(verbose_name='текст статьи')
	product = models.ManyToManyField(Product)

	def __str__(self):
		return self.name

class Cart(models.Model):
	account = models.ForeignKey(Account, on_delete = models.CASCADE)
	product = models.ForeignKey(Product, on_delete = models.CASCADE)
	pr_count = models.IntegerField()

class Order(models.Model):
	account = models.ForeignKey(Account, on_delete = models.CASCADE)
	product = models.ForeignKey(Product, on_delete = models.CASCADE)
	pr_count = models.IntegerField()

	def __str__(self):
		return 'account_' + self.account.name + '__product_' + self.product.name + '_' + str(self.pr_count) + '_pcs'