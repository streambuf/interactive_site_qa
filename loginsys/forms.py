# -*- coding: utf-8 -*-

from django.forms import ModelForm
from loginsys.models import User
from django import forms
from django.utils.translation import gettext as _
from django.core.files.images import get_image_dimensions
from django.core.files.base import ContentFile



class RegisterForm(forms.ModelForm):
	password = forms.CharField(label=_("Пароль"), widget=forms.PasswordInput(),
	error_messages={'required': 'Введите пароль', 'invalid': 'Некорректный пароль'})
	password2 = forms.CharField(label=_("Повторите пароль"), widget=forms.PasswordInput(),
	error_messages={'required': 'Введите пароль', 'invalid': 'Некорректный пароль'})
	username = forms.CharField(label=_("Логин"),max_length=15,
	error_messages={'required': 'Введите логин', 'invalid': 'Некорректный логин'})
	email = forms.EmailField(label=_("Email"),max_length=25,
	error_messages={'required': 'Введите Email', 'invalid': 'Некорректный Email'})
	avatar = forms.ImageField(label=_("Загрузите аватар"), required=False, widget=forms.FileInput,
	error_messages={'invalid': 'Некорректное изображение'})

	class Meta:
		model = User
		fields = ('username', 'email', 'password', 'password2', 'avatar')
		
	def clean_password2(self):
		password = self.cleaned_data.get("password")
		password2 = self.cleaned_data.get("password2")
		if not password2:
			raise forms.ValidationError("Введите повторный пароль")
		if password != password2:
			raise forms.ValidationError("Пароли не совпадают.")	
		
		return self.cleaned_data
		
			
	def clean_avatar(self):
		image = self.cleaned_data['avatar']
		if not image:
			return image
		if image.size > 100*1024:
			raise forms.ValidationError("Слишком большой размер изображения ( > 100Кб )")
		return image
	
		
