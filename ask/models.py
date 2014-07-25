# -*- coding: utf-8 -*-
from django.db import models
from loginsys.models import User
from djangosphinx import SphinxSearch

	
class Tag(models.Model):
	content_tag = models.CharField(max_length=20)
	def __unicode__(self):  
		return self.content_tag
	
class Question(models.Model):
	title = models.CharField(max_length=80)
	content_question = models.TextField()
	creation_date_question = models.DateTimeField()
	question_rating = models.IntegerField(default='0')
	id_user = models.ForeignKey(User, related_name='questions')
	tags = models.ManyToManyField(Tag, related_name='questions')
	user_rate_plus = models.ManyToManyField(User, related_name='q_rate_plus')
	user_rate_minus = models.ManyToManyField(User, related_name='q_rate_minus')
	count_answers = models.IntegerField(default='0')
	search = SphinxSearch(
		index='ask_index',
		weights={
			'title': 100,
			'content_question': 50,
		}
	)
	def __unicode__(self):  
		return self.title
	
class Answer(models.Model):
	content_answer = models.TextField(verbose_name="Введите ваш ответ:")
	creation_date_answer = models.DateTimeField()
	answer_rating = models.IntegerField()
	correct_answer = models.BooleanField(default='0')
	id_user = models.ForeignKey(User, related_name='answers')
	id_question = models.ForeignKey(Question, related_name='answers')
	user_rate_plus = models.ManyToManyField(User, related_name='a_rate_plus')
	user_rate_minus = models.ManyToManyField(User, related_name='a_rate_minus')
	file  = models.FileField(upload_to='files', blank=True)
	def __unicode__(self):  # Python 3: def __str__(self):
		return self.content_answer

class TopUsers(models.Model):
	username = models.CharField(max_length=30)
	old_id = models.IntegerField(default='0')
	
class TopTags(models.Model):
	content_tag = models.CharField(max_length=20)
	old_id = models.IntegerField(default='0')	

	
	
				

