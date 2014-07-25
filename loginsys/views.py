# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf
from loginsys.models import User
from django.template import RequestContext
from loginsys.forms import RegisterForm

def login(request):
	args = {}
	args.update(csrf(request))
	if request.POST:
		username = request.POST.get('username', '')
		password = request.POST.get('password', '')
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request, user)
			return redirect('/ask')
		else:
			args['login_error'] = "Неправильный логин или пароль"
			return render_to_response('loginsys/login.html', args)
			
	else:
		return render_to_response('loginsys/login.html', args, context_instance=RequestContext(request))
		
		
def logout(request):
	auth.logout(request)
	return redirect("/ask")
	
	
def register(request):
	context = RequestContext(request)
	registered = False
	if request.method == 'POST':
		form = RegisterForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			user = form.save()
			user.set_password(user.password)
			#if 'avatar' in request.FILES:
			#	user.avatar = request.FILES['avatar']
			user.save()
			registered = True
		else:
			print form.errors
	else:
		form = RegisterForm()
	return render_to_response('loginsys/register.html', {'form': form, 'registered': registered}, context)
	

def profile(request):
	context = RequestContext(request)
	changed = False
	record = auth.get_user(request)
	form = RegisterForm(initial={'email': 'dfdf'})
	if request.method == 'POST':
		form = RegisterForm(data=request.POST, files=request.FILES, instance=record)
		if form.is_valid():
			user = form.save()
			user.set_password(user.password)
			user.save()
			changed = True
		else:
			print form.errors
	else:
		form = RegisterForm(initial={'username': record.username, 'email': record.email, 'avatar': record.avatar})
	return render_to_response('loginsys/profile.html', {'form': form, 'changed': changed}, context)						

	
									
