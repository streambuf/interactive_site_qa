# -*- coding: utf-8 -*-

from django.shortcuts import get_object_or_404, render_to_response, redirect, render 
from django.http import HttpResponseRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist
from ask.models import Question, Answer, User, Tag
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import auth
from django.db.models import Count
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from datetime import datetime
from forms import AnswerForm, NewAskForm, SearchForm
from django.utils import simplejson
from django.core.mail import send_mail
from smtplib import SMTPRecipientsRefused
from django.template import RequestContext
import logging
from sphinxapi import SphinxClient
import sphinxapi
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


# Список вопросов (вкладка "новые")
def index( request, page_number=1 ):
	args = {}
	try:
		question_list = Question.objects.order_by("-creation_date_question")
		current_page = Paginator(question_list, 20)
		pages = current_page.page(page_number)
		args['question_list'] = pages
		args['user'] = auth.get_user(request)
		args['pop'] = False
	except ObjectDoesNotExist:
		raise Http404
	except EmptyPage:
		raise Http404		
	except PageNotAnInteger:
		raise Http404	
											
	return render_to_response('ask/index.html', args, context_instance=RequestContext(request))

# Список вопросов (вкладка "популярные")
def popindex( request, page_number=1 ):
	args = {}
	try:
		question_list = Question.objects.order_by("-question_rating")
		current_page = Paginator(question_list, 20)
		args['question_list'] = current_page.page(page_number)
		args['user'] = auth.get_user(request)
		args['pop'] = True
	except ObjectDoesNotExist:
		raise Http404
	except EmptyPage:
		raise Http404		
	except PageNotAnInteger:
		raise Http404
	return render_to_response('ask/index.html', args, context_instance=RequestContext(request))	

# Задать вопрос
def ask( request, id, page_number=1 ):
	try:
		answer_form = AnswerForm
		args = {}
		args.update(csrf(request))
	
		args['question'] = Question.objects.get(id=id)
		answers = Answer.objects.filter(id_question=id).order_by("-correct_answer","-answer_rating", "-creation_date_answer")
		current_page = Paginator(answers, 30)
		pages = current_page.page(page_number)
		args['answers'] = pages
		args['form'] = answer_form
		args['user'] = auth.get_user(request)
	except ObjectDoesNotExist:
		raise Http404
	except EmptyPage:
		raise Http404		
	except PageNotAnInteger:
		raise Http404		
	
	return render_to_response('ask/ask.html', args, context_instance=RequestContext(request))


# Вопросы с фильтрацией по тегу	
def tags( request, id, page_number=1 ):
	args = {}
	try:
		question_list = Question.objects.filter(tags__id = id).order_by("-question_rating", "-creation_date_question")
		current_page = Paginator(question_list, 20)
		args['question_list'] = current_page.page(page_number)
		args['user'] = auth.get_user(request)
		args['pop'] = False
		args['tag'] = Tag.objects.get(id=id)
	except ObjectDoesNotExist:
		raise Http404
	except EmptyPage:
		raise Http404		
	except PageNotAnInteger:
		raise Http404		
	
	return render_to_response('ask/tags.html', args, context_instance=RequestContext(request))	
	

# Повысить рейтинг вопросу
def qplus(request):
	context = RequestContext(request)
	if request.method == 'GET':
		qid = request.GET.get('qid')
		
	if qid:
		question = Question.objects.get(id=int(qid))
		if question and question.id_user_id != request.user.id:
			
			if not question.user_rate_plus.filter(id = request.user.id).exists():
				question.question_rating += 1
					
				
				if question.user_rate_minus.filter(id = request.user.id).exists():
					question.user_rate_minus.remove(request.user)
				else:
					question.user_rate_plus.add(request.user)	
					
				question.save()	
			
			resp = {"status": "ok", "data": question.question_rating}
		resp = {"status": "error", "message":"The user can not vote for themselves", "data": question.question_rating}	
	else:
		resp = {"status": "error", "message":"No qid sent", "data": question.question_rating}
	return HttpResponse(simplejson.dumps(resp),
					mimetype='application/javascript')


# Понизить рейтинг вопросу	
def qminus( request):
	context = RequestContext(request)
	if request.method == 'GET':
		qid = request.GET.get('qid')
		
	if qid:
		question = Question.objects.get(id=int(qid))
		if question and question.id_user_id != request.user.id:
			
			if not question.user_rate_minus.filter(id = request.user.id).exists():
				question.question_rating -= 1
				
				
				if question.user_rate_plus.filter(id = request.user.id).exists():
					question.user_rate_plus.remove(request.user)
					
				else:
					question.user_rate_minus.add(request.user)
					
					
			question.save()		
			
			resp = {"status": "ok", "data": question.question_rating}
		resp = {"status": "error", "message":"The user can not vote for themselves", "data": question.question_rating}	
	else:
		resp = {"status": "error", "message":"No qid sent", "data": question.question_rating}
	return HttpResponse(simplejson.dumps(resp),
					mimetype='application/javascript')
	
	
				
	return HttpResponse(simplejson.dumps(resp),
					mimetype='application/javascript')
					

# Повысить рейтинг ответу
def aplus(request):
	try:
		context = RequestContext(request)
		if request.method == 'GET':
			aid = request.GET.get('aid')
			
		if aid:
			answer = Answer.objects.get(id=int(aid))
			if answer and answer.id_user_id != request.user.id:
			
				if not answer.user_rate_plus.filter(id = request.user.id).exists():
					answer.answer_rating += 1
						
					
					if answer.user_rate_minus.filter(id = request.user.id).exists():
						answer.user_rate_minus.remove(request.user)
					else:
						answer.user_rate_plus.add(request.user)	
						
					answer.save()	
				
				resp = {"status": "ok", "data": answer.answer_rating}
			resp = {"status": "error", "message":"The user can not vote for themselves", "data": answer.answer_rating}	
		else:
			resp = {"status": "error", "message":"No qid sent", "data": answer.answer_rating}
	except ObjectDoesNotExist:
		raise Http404	
				
	return HttpResponse(simplejson.dumps(resp),
					mimetype='application/javascript')


# Понизить рейтинг ответу	
def aminus( request):
	try:
		context = RequestContext(request)
		if request.method == 'GET':
			aid = request.GET.get('aid')
			
		if aid:
			answer = Answer.objects.get(id=int(aid))
			if answer and answer.id_user_id != request.user.id:
				
				if not answer.user_rate_minus.filter(id = request.user.id).exists():
					answer.answer_rating -= 1
					
					
					if answer.user_rate_plus.filter(id = request.user.id).exists():
						answer.user_rate_plus.remove(request.user)
					else:
						answer.user_rate_minus.add(request.user)
						
					answer.save()		
				
				resp = {"status": "ok", "data": answer.answer_rating}
			resp = {"status": "error", "message":"The user can not vote for themselves", "data": answer.answer_rating}		
		else:
			resp = {"status": "error", "message":"No qid sent", "data": answer.answer_rating}
	except ObjectDoesNotExist:
		raise Http404	
				
	return HttpResponse(simplejson.dumps(resp),
					mimetype='application/javascript')					
					

# Отметить ответ "лучшим"
def correct( request):
	try:
		context = RequestContext(request)
		if request.method == 'GET':
			aid = request.GET.get('aid')
			qid = request.GET.get('qid')
			
		if aid and qid:
			answer = Answer.objects.get(id=int(aid))
			answers = Answer.objects.filter(id_question=int(qid))
			for a in answers:
				a.correct_answer = 0
				a.save()
			if answer:
				if answer.correct_answer == True:
					answer.correct_answer = False
				else:
					answer.correct_answer = True
				answer.save()		
					
				resp = {"status": "ok", "data": answer.correct_answer, "qid": qid}
		else:
			resp = {"status": "error", "message":"No aid or qid sent"}
	except ObjectDoesNotExist:
		raise Http404			
	return HttpResponse(simplejson.dumps(resp),
					mimetype='application/javascript')					



# Добавить комментарий	
def addcomment(request, id):
	if request.POST:
		form = AnswerForm(request.POST)
		if form.is_valid():
			try:
				answer = form.save(commit=False)
				answer.id_question = Question.objects.get(id=id)
				answer.creation_date_answer = datetime.now()
				answer.answer_rating = 0
				answer.correct_answer = 0
				user = User.objects.get(id=request.user.id)
				answer.id_user = user
				form.save()
				question = Question.objects.get(id=id)
				question.count_answers += 1
				question.save()
				try:
					send_mail('Вы получиили ответ на ваш вопрос: ',
					'Перейти на страницу вопроса: http://127.0.0.1/ask/' + str(id), 'streambuf@mail.ru', [question.id_user.email])
				except SMTPRecipientsRefused:
					return redirect('/ask/%s/' % id)
			except ObjectDoesNotExist:
				raise Http404				
	return redirect('/ask/%s/' % id)	


# Задать новый вопрос	
def newask(request):
	if request.method == 'POST':
		form = NewAskForm(request.POST)
		if form.is_valid():
			try:
				title = form.cleaned_data['title']
				content_question = form.cleaned_data['content_question']
				user_id = request.user.id
				newask = Question.objects.create(title = title, content_question = content_question, id_user_id = user_id, creation_date_question = datetime.now())
				string_tags = form.cleaned_data['tags']
				list_tags = string_tags.split(",")
				for tag in list_tags:
					tag = tag.strip()
					tag_object = Tag.objects.filter(content_tag = tag)
					if tag_object.count() > 0:
						tag_object[0].save()
						newask.tags.add(tag_object[0])
					else:
						new_tag = Tag.objects.create(content_tag = tag)
						new_tag.save()
						newask.tags.add(new_tag)
					newask.save()
			except ObjectDoesNotExist:
				raise Http404			
			return HttpResponseRedirect('/ask')
		else:
			print form.errors

	else:
		form = NewAskForm()
		
	return render(request, 'ask/newask.html', {'form': form })
	

# Поиск по вопросам и комментариям	
def search(request, page_number=1):
	if request.method == 'GET':
		form = SearchForm(request.GET)
		
		try:
			query = request.GET.get('q', '')
			
			weights = {
			'title': 100,
			'content_question': 80
			}

			# подключение 
			c = sphinxapi.SphinxClient()
			c.SetServer('localhost', 9845)
			c.SetConnectTimeout(2.0)
			if c.Status():
				# режим совпадения слов из запроса с существующими статьями
				c.SetMatchMode(sphinxapi.SPH_MATCH_ANY)

				# режим сортировки
				c.SetSortMode(sphinxapi.SPH_SORT_RELEVANCE)

				# веса для полей модели
				c.SetFieldWeights(weights)

				# ограничить результат 30 совпадениями
				c.SetLimits(0, 1000)

				# поиск слова django по индексу 
				result = c.Query(query, 'ask_index ask_index2')
				total = result['total']

				# выборка объектов
				ids = [obj['id'] for obj in result['matches']]

				args = {}
				questions = Question.objects.filter(id__in=ids)
				
				current_page = Paginator(questions, 30)
				question_list = current_page.page(page_number)
				
				return render(request, 'ask/search.html',
							  {'question_list': question_list, 'total' : total,
							   'query': query, 'form': form})
			else:
				args['error_status'] = True
				return render(request, 'ask/search.html', {'form': form})
		except ObjectDoesNotExist:
			raise Http404	
		except EmptyPage:
			raise Http404		
		except PageNotAnInteger:
			raise Http404		
	else:
		form = SearchForm()
		return render(request, 'ask/search.html', {'form': form})	

