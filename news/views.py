# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaultfilters import slugify
import hashlib
from news.models import *
from news.forms import *

import urllib, hashlib
import datetime

# views_dashboard have dashboard views requests
from views_dashboard import *



'''
File: views.pl
Author: Rafal Gawlik
Description: File content view used in app
Created: 13.11.2014 Wroclaw

index
blog
user
post
logout_page
register_page
'''

# Request supports main page
# Features: list last post and other
# Link: /
# Template: index.html
def index(request):
   news = News.objects.all().order_by('-posted_date')[:5]
   if request.user.is_authenticated():
      name = request.user.get_username()
      return render_to_response('index.html', {'news': news, }, context_instance=RequestContext(request))
   else:
      return render_to_response('index.html', {'news': news, }, context_instance=RequestContext(request))


# Request supports blog page
# Features: supports the main blog page
# Link: /<blog.slug>
# Template: blog.html
def blog(request, slug):
   news_list = News.objects.filter(blog__slug = slug).order_by('-posted_date')
   blog = Blog.objects.get(slug = slug)

   paginator = Paginator(news_list, 5)
   page = request.GET.get('page')

   try:
      news = paginator.page(page)
   except PageNotAnInteger:
      # If page is not an integer, deliver first page.
      news = paginator.page(1)
   except EmptyPage:
      # If page is out of range (e.g. 9999), deliver last page of results.
      news = paginator.page(paginator.num_pages)

   return render_to_response('blog.html', {'news': news, 'blog': blog }, context_instance=RequestContext(request))


# Request supports user page
# Features: supports the user public page
# Link: /user/<user.slug>
# Template: user.html
def user(request, slug):
   user_portal = User.objects.get(username = slug)
   blogs = Blog.objects.filter(user__username = slug)

   #perform user avatar
   email_hash = hashlib.md5(user_portal.email.strip().lower()).hexdigest()
   url = "http://www.gravatar.com/avatar/%s?s=300" % email_hash

   try:
      user_details = UserDetails.objects.get(user__username = slug)
      return render_to_response('user.html', {'blog': blogs ,
        'user_portal' : user_portal , 'user_details' : user_details ,
        'url':url }, context_instance=RequestContext(request))
   except UserDetails.DoesNotExist:
      return render_to_response('user.html', {'blog': blogs ,
        'user_portal' : user_portal , 'url':url }, context_instance=RequestContext(request))


# Request supports post page
# Features: supports the post page
# Link: /<blog.slug>/<post.id>
# Template: post.html
def post(request, slug, id):
   if request.method == 'GET':
      news = News.objects.get(id = id, blog__slug = slug)
      # comments = Comment.objects.filter(news = news, status = True).order_by('-posted_date')
      comments = Comment.objects.filter(news = news).order_by('-posted_date')

      return render_to_response('post.html', {'news': news , 'comments':comments }, context_instance=RequestContext(request))
   elif request.method == 'POST': #handling POST HTTP request
      news = News.objects.get(id = id, blog__slug = slug)

      if "text_comment" in request.POST:
         name = request.user.get_username()

         # handle user object from session
         u = User.objects.get(username=name)
         text = request.POST.get("text_comment", "")

         # perform date for new blog
         date = datetime.date.today()
         time =  datetime.datetime.now()

         comment = Comment.objects.create(text=text,
            slug='%i-%i-%i-%i-%i-%i-%s' % (date.year, date.month, date.day,
                time.hour, time.minute, time.second, slugify(text)),
            user=u, news=news)

         comments = Comment.objects.filter(news = news, status = True).order_by('-posted_date')

         return HttpResponseRedirect("/"+slug+"/"+id)
      else:
         comments = Comment.objects.filter(news = news).order_by('-posted_date')
         return render_to_response('post.html', {'news': news ,
            'comments':comments }, context_instance=RequestContext(request))



# Request supports logout page
# Features: supports the logout page
# Link: /logout
# Template: #
def logout_page(request):
   logout(request)
   return HttpResponseRedirect("/")


# Request supports registry page
# Features: supports the registry page
# Link: /register
# Template: registration/register.html
def register_page(request):
   if request.method == 'POST':
      form = FormularzRejestracji(request.POST)
      if form.is_valid():
         user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email']
         )
         user.last_name = form.cleaned_data['phone']
         user.save()
         if form.cleaned_data['log_on']:
            user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password1'])
            login(request,user)
            template = get_template("main_page.html")
            variables = RequestContext(request,{'user':user})
            output = template.render(variables)
            return HttpResponseRedirect("/")
         else:
            template = get_template("registration/register_success.html")
            variables = RequestContext(request,{'username':form.cleaned_data['username']})
            output = template.render(variables)
            return HttpResponse(output)
   else:
      form = FormularzRejestracji()

   template = get_template("registration/register.html")
   variables = RequestContext(request,{'form':form})
   output = template.render(variables)
   return HttpResponse(output)
