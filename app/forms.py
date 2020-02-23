from django import forms
from .models import Account

class RegisterForm(forms.Form):
	name = forms.EmailField(label='Адрес электронной почты:')
	password = forms.CharField(label='Придумайте пароль:', widget=forms.PasswordInput())
	password_again = forms.CharField(label='Повторите пароль:', widget=forms.PasswordInput())

	def clean_name(self):
		name = self.cleaned_data['name']
		return name

	def clean_password(self):
		password = self.cleaned_data['password']
		return password

	def clean_password_again(self):
		password_again = self.cleaned_data['password_again']
		return password_again

	class Meta(object):
		model = Account
		fields = ('name', 'password')

class AuthorisationForm(forms.Form):
	name = forms.CharField(label='Адрес электронной почты:')
	password = forms.CharField(label='Пароль:', widget=forms.PasswordInput())

	def clean_name(self):
		name = self.cleaned_data['name']
		return name

	def clean_password(self):
		password = self.cleaned_data['password']
		return password

	class Meta(object):
		model = Account
		fields = ('name', 'password')

class HiddenCartForm(forms.Form):
	
	name = forms.CharField(widget = forms.HiddenInput(), required = False)

	def clean_name(self):
		name = self.cleaned_data['name']
		return name
