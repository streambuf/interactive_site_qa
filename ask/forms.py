# -*- coding: utf-8 -*-
from django.forms import ModelForm
from models import Answer
from django import forms

# Форма ответа
class AnswerForm(ModelForm):
	file = forms.FileField(required=False, widget=forms.FileInput)
	class Meta:
		model = Answer
		fields = ['content_answer']
		
		
# Форма добавления вопроса
class NewAskForm(forms.Form):
	title = forms.CharField(max_length=80)
	content_question = forms.CharField()
	tags = forms.CharField(max_length=200, required=False)
	
	def clean_tags(self):
		string_tags = self.cleaned_data['tags']
		list_tags = string_tags.split(",")
		count = 0
		for tag in list_tags:
			count += 1
			if count > 3:
				raise forms.ValidationError("Нельзя добавлять больше трех тегов")
		return string_tags	
		
# Форма поиска
class SearchForm(forms.Form):
    q = forms.CharField(max_length=255)			
