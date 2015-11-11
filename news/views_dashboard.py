# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaultfilters import slugify

from news.models import *
from news.forms import *

import urllib, hashlib
import datetime
import hashlib


'''
File: views_dashboard.pl
Author: Rafal Gawlik
Description: File content dashboard views
Created: 5.11.2014 Wroclaw

dashboard
dashboard_blogs
dashboard_blogs_configuration
dashboard_blog_post
dashboard_post
dashboard_comments
dashboard_user_settings
upload_image
save_file
'''


# Request supports dashboard
# Features: add post, check auterization
# TODO add notification, comments, publishger news entryies
# Główna strona kokpitu
# Link: /dashboard
# Template: dashboard/index.html
def dashboard(request):
    if request.method == 'GET': # handling GET HTTP request
        if request.user.is_authenticated():
            name = request.user.get_username()
            blogs = Blog.objects.filter(user__username = name)# blogs of loged user
            publisherNews = PublisherNews.objects.all().order_by('-posted_date')[:5]
            return render_to_response('dashboard/index.html', { 'blog': blogs , 'publisherNews':publisherNews },
                context_instance=RequestContext(request))
        else: # check user isn't loged -> return to main
            return HttpResponseRedirect("/")
    elif request.method == 'POST': #handling POST HTTP request
        if request.user.is_authenticated():
            if "add_post" in request.POST:
                name = request.user.get_username()
                publisherNews = PublisherNews.objects.all().order_by('-posted_date')[:5]
                blogs = Blog.objects.filter(user__username = name) #blogs of loged user

                # handing request properties
                title = request.POST.get("post_title", "")
                description = request.POST.get("post_description", "")
                text = request.POST.get("post_content", "")
                blog_title = request.POST.get("post_blog", "")

                blog = None
                for b in blogs:
                    if b.name == blog_title:
                        blog = b

                if (blog == None) | (title == None) :
                    notification = '<strong> ERROR </strong> błąd przy publikowaniu wpisu :('
                    return render_to_response('dashboard/index.html', { 'blog': blogs,
                        'notification' : notification }, context_instance=RequestContext(request))

                # perform date for post slug
                date = datetime.date.today()
                time =  datetime.datetime.now()

                # create new News object ORM
                news = News.objects.create(title=title, description=description,
                    slug='%i-%i-%i-%i-%i-%i-%s' % (date.year, date.month, date.day,
                    time.hour, time.minute, time.second, slugify(title)),
                text=text, blog=blog)

                # show notofication
                notification = '<strong>' + title + '</strong> posted successfully! :)'
                #TODO clean request
                return render_to_response('dashboard/index.html', { 'blog': blogs,
                    'notification' : notification, 'publisherNews':publisherNews}, context_instance=RequestContext(request))
            else:
                return HttpResponseRedirect("/dashboard/")
    else: # check user isn't loged -> return to main
        return HttpResponseRedirect("/")



# Request supports dashboard blogs list
# Features: blog list, add new blog
# TODO notification entries
# Link: /dashboard/blogs
# Template: dashboard/blogs.html
def dashboard_blogs(request):
    if request.method == 'GET': # handling GET HTTP request
        if request.user.is_authenticated():
            name = request.user.get_username()
            publisherNews = PublisherNews.objects.all().order_by('-posted_date')[:5]
            blogs = Blog.objects.filter(user__username = name) # blogs logged user
            return render_to_response('dashboard/blogs.html', { 'blog': blogs , 'publisherNews':publisherNews },
                context_instance=RequestContext(request))
        else: # check user isn't loged -> return to main
            return render_to_response('index.html', {}, context_instance=RequestContext(request))
    elif request.method == 'POST': # handling POST HTTP request
        if request.user.is_authenticated():

            if "view" in request.POST:
                slug = request.POST.get("view", "");
                return HttpResponseRedirect("/dashboard/blogs/" + slug)
            elif "edit" in request.POST:
                slug = request.POST.get("edit", "");
                return HttpResponseRedirect("/dashboard/blogs/" + slug + "/configuration");
            elif "comments" in request.POST:
                slug = request.POST.get("comments", "");
                return HttpResponseRedirect("/dashboard/comments/" + slug );
            elif "delete" in request.POST:
                slug = request.POST.get("delete", "");
                return HttpResponseRedirect("/dashboard/blogs/" + slug +"/delete");

            elif "blog_title" in request.POST:
                name = request.user.get_username()
                publisherNews = PublisherNews.objects.all().order_by('-posted_date')[:5]
                blogs = Blog.objects.filter(user__username = name) # blogs logged user

                # handing request properties
                name = request.POST.get("blog_title", "")
                slug = request.POST.get("blog_slug", "")
                description = request.POST.get("blog_description", "")

                if (name == "") | (slug == ""):
                    notification = '<strong> nazwa i odnośnik </strong> nie mogą byc puste :)'
                    return render_to_response('dashboard/blogs.html', { 'blog': blogs,
                        'notification' : notification , 'publisherNews':publisherNews }, context_instance=RequestContext(request))

                # perform date for new blog
                date = datetime.date.today()
                time =  datetime.datetime.now()

                # create new Blog object ORM
                blog = Blog.objects.create(name=name, description=description, slug=slugify(slug), user = request.user)

                # notification  for web
                notification = '<strong>' + name + '</strong> created successfully! :)'
                return render_to_response('dashboard/blogs.html', { 'blog': blogs,
                    'notification' : notification , 'publisherNews':publisherNews }, context_instance=RequestContext(request))
            else:
                return HttpResponseRedirect("/");

    else: # check user isn't loged -> return to main
        return render_to_response('index.html', {}, context_instance=RequestContext(request))


# Request supports dashboard blogs configuration
# Features: for specyfyfic blog - change data
# TODO all view!!!
# TEST
# Link: dashboard/blogs/<blog.slug>/configuration
# Template: dashboard/blogs_configuration.htm
def dashboard_blogs_configuration(request, slug):
    if request.method == 'GET': # handling GET HTTP request
        if request.user.is_authenticated():
            blog = Blog.objects.get(slug = slug)
            return render_to_response('dashboard/blogs_configuration.html', { 'blog':blog }, context_instance=RequestContext(request))
        else: # check user isn't loged -> return to main
            return render_to_response('index.html', {}, context_instance=RequestContext(request))
    elif request.method == 'POST': # handling POST HTTP request
        if request.user.is_authenticated():
            return render_to_response('dashboard/blogs_configuration.html', { }, context_instance=RequestContext(request))
        else: # check user isn't loged -> return to main
            return render_to_response('index.html', {}, context_instance=RequestContext(request))


def dashboard_blogs_delete(request, slug):
    if request.method == 'GET': # handling GET HTTP request
        if request.user.is_authenticated():

            blog = Blog.objects.get(slug = slug)

            return render_to_response('dashboard/blogs_delete.html', { 'blog':blog }, context_instance=RequestContext(request))
        else: # check user isn't loged -> return to main
            return render_to_response('index.html', {}, context_instance=RequestContext(request))
    elif request.method == 'POST': # handling POST HTTP request
        if request.user.is_authenticated():
            blog = Blog.objects.get(slug = slug)

            if "yes" in request.POST:
                blog.delete()
                return HttpResponseRedirect("/dashboard/blogs/")
            else:
                return HttpResponseRedirect("/dashboard/blogs/")
        else: # check user isn't loged -> return to main
            return render_to_response('index.html', {}, context_instance=RequestContext(request))


# Request supports dashboard blog - post list
# Features: post list, configuration link,
# TEST
# Link: dashboard/post/<post.slug>/delete
# Template: dashboard/blog_posts.html
def dashboard_post_delete(request, slug):
    # if request.method == 'GET': # handling GET HTTP request
    #     if request.user.is_authenticated():
    #
    #         post = News.objects.get(slug = slug)
    #
    #         return render_to_response('dashboard/post_delete.html', { 'post':post }, context_instance=RequestContext(request))
    #     else: # check user isn't loged -> return to main
            return render_to_response('index.html', {}, context_instance=RequestContext(request))
    # elif request.method == 'POST': # handling POST HTTP request
        # if request.user.is_authenticated():
        #     post = News.objects.get(slug = slug)
        #
        #     if "yes" in request.POST:
        #         post.delete()
        #         return HttpResponseRedirect("/dashboard/")
        #     else:
        #         return HttpResponseRedirect("/dashboard/")
        # else: # check user isn't loged -> return to main
            # return render_to_response('index.html', {}, context_instance=RequestContext(request))


# Request supports dashboard blog - post list
# Features: post list, configuration link,
# TODO comments, edit/remove post, approve/remove comment,
# TEST
# Link: dashboard/post/<post.slug>
# Template: dashboard/blog_posts.html
def dashboard_blog_post(request, slug):
    if request.method == 'GET': # handling GET HTTP request
        if request.user.is_authenticated():
            publisherNews = PublisherNews.objects.all().order_by('-posted_date')[:5]
            blog = Blog.objects.get(slug = slug) # localize blog
            news = News.objects.all().filter(blog = blog).order_by('-posted_date') # extract news from blog

            paginator = Paginator(news, 5)
            page = request.GET.get('page')

            try:
                news = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                news = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                news = paginator.page(paginator.num_pages)



            return render_to_response('dashboard/blog_posts.html', { 'blog':blog,
                'news':news , 'publisherNews':publisherNews },
                context_instance=RequestContext(request))
        else: # check user isn't loged -> return to main
            return render_to_response('index.html', {}, context_instance=RequestContext(request))
    elif request.method == 'POST': # handling POST HTTP request
        if request.user.is_authenticated():
            blog = Blog.objects.get(slug = slug) # localize blog
            publisherNews = PublisherNews.objects.all().order_by('-posted_date')[:5]
            news = News.objects.all().filter(blog = blog) # extract news from blog

            if "post_title" in request.POST:
                title = request.POST.get("post_title", "")
                description = request.POST.get("post_description", "")
                text = request.POST.get("post_content", "")

                if title == "" :
                    notification = '<strong> ERROR </strong> błąd przy publikowaniu wpisu :('
                    return render_to_response('dashboard/blog_posts.html', { 'blog':blog,
                        'news' : news , 'notification' : notification,
                        'publisherNews' : publisherNews},
                        context_instance=RequestContext(request))


                # perform date for new blog
                date = datetime.date.today()
                time =  datetime.datetime.now()

                news_new = News.objects.create(title=title, description=description,
                    slug='%i-%i-%i-%i-%i-%i-%s' % (date.year, date.month,
                    date.day, time.hour, time.minute, time.second, slugify(title)),
                    text=text, blog=blog)

                news = News.objects.all().filter(blog = blog) # extract news from blog actualize
                notification = '<strong> Sukces </strong> pomyslnie opublikowano :)'
                return render_to_response('dashboard/blog_posts.html', { 'blog':blog,
                    'news':news, 'notification':notification,
                    'publisherNews':publisherNews},
                    context_instance=RequestContext(request))
            elif "blog_title_form" in request.POST:
                name = request.POST.get("blog_title_form", "")
                slug_new = request.POST.get("blog_slug_form", "")
                description = request.POST.get("blog_description_form", "")
                background_image = request.POST.get("background_image_form", "")
                comments_moderate = request.POST.get("comments_moderate", "")

                blog.name = name
                blog.slug = slug_new
                blog.description = description
                blog.background_image = background_image
                blog.comment_moderate = comments_moderate
                blog.save()

                notification = '<strong> Zmieniono bloga </strong> :)'
                return render_to_response('dashboard/blog_posts.html', { 'blog':blog,
                    'news':news, 'notification':notification,
                    'publisherNews':publisherNews},
                    context_instance=RequestContext(request))

            elif "view" in request.POST:
                id_post = request.POST.get("view", "")
                return HttpResponseRedirect("/"+slug+"/"+id_post)

            elif "edit" in request.POST:
                slug_comment = request.POST.get("edit", "")
                return HttpResponseRedirect("/dashboard/post/"+slug_comment)

            elif "comments" in request.POST:
                # TODO
                #slug_comment = request.POST.get("remove", "")
                #comment =  Comment.objects.get(slug = slug_comment)
                #comment.delete()
                news_slug = request.POST.get("comments", "")
                return HttpResponseRedirect("/dashboard/comments/"+blog.slug+"/"+news_slug)

            elif "delete" in request.POST:
                news_slug = request.POST.get("delete", "")
                news = News.objects.all().filter(slug = news_slug)
                news.delete()
                # TODO
                #slug_comment = request.POST.get("remove", "")
                #comment =  Comment.objects.get(slug = slug_comment)
                #comment.delete()
                return HttpResponseRedirect("/dashboard/blogs")

    else: # check user isn't loged -> return to main
        return render_to_response('index.html', {}, context_instance=RequestContext(request))


# Request supports dashboard post - edition/remove
# Features: edite/remove post
# TODO all view!!!
# TEST
# Link: dashboard/post/<post.slug>
# Template: dashboard/post.html
def dashboard_post(request, slug):
    if request.method == 'GET': # handling GET HTTP request
        if request.user.is_authenticated():
            news = News.objects.get(slug = slug) # localize news
            name = request.user.get_username()
            publisherNews = PublisherNews.objects.all().order_by('-posted_date')[:5]
            blogs = Blog.objects.filter(user__username = name)
            return render_to_response('dashboard/post.html', { 'news':news, 'blog':blogs,
                'publisherNews':publisherNews}, context_instance=RequestContext(request))
        else: # check user isn't loged -> return to main
            return render_to_response('index.html', {}, context_instance=RequestContext(request))
    elif request.method == 'POST': # handling POST HTTP request
        if request.user.is_authenticated():
            publisherNews = PublisherNews.objects.all().order_by('-posted_date')[:5]

            name = request.user.get_username()
            publisherNews = PublisherNews.objects.all().order_by('-posted_date')[:5]
            blogs = Blog.objects.filter(user__username = name) #blogs of loged user

            # handing request properties
            title = request.POST.get("post_title", "")
            description = request.POST.get("post_description", "")
            text = request.POST.get("post_content", "")
            blog_title = request.POST.get("post_blog", "")


            for b in blogs:
                blog = None
                if b.name == blog_title:
                    blog = b

            if (blog == None) | (title == None) :
                notification = '<strong> ERROR </strong> błąd przy publikowaniu wpisu :('
                return render_to_response('dashboard/index.html', { 'blog': blogs,
                    'notification' : notification }, context_instance=RequestContext(request))

            # perform date for post slug
            date = datetime.date.today()
            time =  datetime.datetime.now()

            news = News.objects.get(slug = slug)
            news.title = title
            news.description = description
            news.text = text
            news.blog = blog
            news.save()


            return HttpResponseRedirect("/dashboard/")
        else: # check user isn't loged -> return to main
            return render_to_response('index.html', {}, context_instance=RequestContext(request))


# Request supports dashboard comments
# Features: edite/remove comments
# TODO notification entries
# Link: /dashboard/comments/
# Template: dashboard/comments.html
def dashboard_comments(request):
    if request.method == 'GET': # handling GET HTTP request
        if request.user.is_authenticated():
            name = request.user.get_username()
            publisherNews = PublisherNews.objects.all().order_by('-posted_date')[:5]
            blogs = Blog.objects.filter(user__username = name)
            comments = Comment.objects.filter(news__blog__user__username = name).order_by('status', '-posted_date')

            paginator = Paginator(comments, 5)
            page = request.GET.get('page')

            try:
               comments_page = paginator.page(page)
            except PageNotAnInteger:
               # If page is not an integer, deliver first page.
               comments_page = paginator.page(1)
            except EmptyPage:
               # If page is out of range (e.g. 9999), deliver last page of results.
               comments_page = paginator.page(paginator.num_pages)


            return render_to_response('dashboard/comments.html', { 'blog': blogs,
                'comments' : comments_page, 'publisherNews':publisherNews
                }, context_instance=RequestContext(request))
        else: # check user isn't loged -> return to main
            return render_to_response('index.html', {}, context_instance=RequestContext(request))
    elif request.method == 'POST': # handling POST HTTP request
        if request.user.is_authenticated():
            name = request.user.get_username()
            publisherNews = PublisherNews.objects.all().order_by('-posted_date')[:5]
            blogs = Blog.objects.filter(user__username = name)
            comments = Comment.objects.filter(news__blog__user__username = name).order_by('status', '-posted_date')

            paginator = Paginator(comments, 5)
            page = request.GET.get('page')

            try:
               comments_page = paginator.page(page)
            except PageNotAnInteger:
               # If page is not an integer, deliver first page.
               comments_page = paginator.page(1)
            except EmptyPage:
               # If page is out of range (e.g. 9999), deliver last page of results.
               comments_page = paginator.page(paginator.num_pages)


            if "accept" in request.POST:
                slug_comment = request.POST.get("accept", "")
                comment =  Comment.objects.get(slug = slug_comment)
                comment.status = True
                comment.save()

            elif "hidden" in request.POST:
                slug_comment = request.POST.get("hidden", "")
                comment =  Comment.objects.get(slug = slug_comment)
                comment.status = False
                comment.save()

            elif "remove" in request.POST:
                slug_comment = request.POST.get("remove", "")
                comment =  Comment.objects.get(slug = slug_comment)
                comment.delete()


            return render_to_response('dashboard/comments.html', { 'blog': blogs,
                'comments' : comments_page, 'publisherNews':publisherNews},
                context_instance=RequestContext(request))
        else: # check user isn't loged -> return to main
            return render_to_response('index.html', {}, context_instance=RequestContext(request))


# Request supports dashboard comments
# Features: edite/remove comments
# TODO notification entries
# Link: /dashboard/comments/<blog.slug>
# Template: dashboard/comments.html
def dashboard_comments_blog(request, slug):
    if request.method == 'GET': # handling GET HTTP request
        if request.user.is_authenticated():
            name = request.user.get_username()
            publisherNews = PublisherNews.objects.all().order_by('-posted_date')[:5]
            blogs = Blog.objects.filter(user__username = name)
            comments = Comment.objects.filter(news__blog__slug = slug).order_by('status', '-posted_date')

            paginator = Paginator(comments, 5)
            page = request.GET.get('page')

            try:
               comments_page = paginator.page(page)
            except PageNotAnInteger:
               # If page is not an integer, deliver first page.
               comments_page = paginator.page(1)
            except EmptyPage:
               # If page is out of range (e.g. 9999), deliver last page of results.
               comments_page = paginator.page(paginator.num_pages)


            return render_to_response('dashboard/comments.html', { 'blog': blogs,
                'comments' : comments_page, 'publisherNews':publisherNews
                }, context_instance=RequestContext(request))
        else: # check user isn't loged -> return to main
            return render_to_response('index.html', {}, context_instance=RequestContext(request))
    elif request.method == 'POST': # handling POST HTTP request
        return render_to_response('index.html', {}, context_instance=RequestContext(request))
    else: # check user isn't loged -> return to main
        return render_to_response('index.html', {}, context_instance=RequestContext(request))


# Request supports dashboard comments
# Features: edite/remove comments
# TODO notification entries
# Link: /dashboard/comments/<blog.slug>/<news.slug>
# Template: dashboard/comments.html
def dashboard_comments_post(request, slug_blog, slug_post):
    if request.method == 'GET': # handling GET HTTP request
        if request.user.is_authenticated():
            name = request.user.get_username()
            publisherNews = PublisherNews.objects.all().order_by('-posted_date')[:5]
            blog = Blog.objects.get(slug = slug_blog) # localize blog
            news = News.objects.get(slug = slug_post) # localize post
            comments = Comment.objects.filter(news__slug = slug_post).order_by('status', '-posted_date')

            paginator = Paginator(comments, 5)
            page = request.GET.get('page')

            try:
               comments_page = paginator.page(page)
            except PageNotAnInteger:
               # If page is not an integer, deliver first page.
               comments_page = paginator.page(1)
            except EmptyPage:
               # If page is out of range (e.g. 9999), deliver last page of results.
               comments_page = paginator.page(paginator.num_pages)


            return render_to_response('dashboard/comments.html', { 'blog': blog, 'news': news,
                'comments' : comments_page, 'publisherNews':publisherNews
                }, context_instance=RequestContext(request))
        else: # check user isn't loged -> return to main
            return render_to_response('index.html', {}, context_instance=RequestContext(request))
    elif request.method == 'POST': # handling POST HTTP request
        return render_to_response('index.html', {}, context_instance=RequestContext(request))
    else: # check user isn't loged -> return to main
        return render_to_response('index.html', {}, context_instance=RequestContext(request))


# Request supports dashboard user settings
# Features: edit first and last name, motto, about
# TODO icon image
# TEST
# Link: dashboard/usersettings/
# Template: dashboard/user_settings.html
def dashboard_user_settings(request):
    publisherNews = PublisherNews.objects.all().order_by('-posted_date')[:5]
    if request.method == 'GET': # handling GET HTTP request
        if request.user.is_authenticated():
            name = request.user.get_username()
            u = User.objects.get(username=name) # get user object from session

            if u.first_name :
                try:
                    user_details = UserDetails.objects.get(user=u) # get UserDetails object from User object
                    return render_to_response('dashboard/user_settings.html', {
                        'first_name' : u.first_name, 'last_name' : u.last_name,
                        'about' : user_details.about, 'motto' : user_details.title,
                        'background_image' : user_details.background_image,
                        'publisherNews':publisherNews
                        }, context_instance=RequestContext(request))
                except UserDetails.DoesNotExist:
                    return render_to_response('dashboard/user_settings.html', {
                        'first_name' : u.first_name, 'last_name' : u.last_name,
                        'publisherNews' : publisherNews
                        }, context_instance=RequestContext(request))
            else:
                return render_to_response('dashboard/user_settings.html', {
                    'publisherNews' : publisherNews }, context_instance=RequestContext(request))
        else: # check user isn't loged -> return to main
            return render_to_response('index.html', {}, context_instance=RequestContext(request))
    elif request.method == 'POST': # handling POST HTTP request
        if request.user.is_authenticated():
            name = request.user.get_username()

        # handle user object from session
        u = User.objects.get(username=name)

        if "first_name" in request.POST:
            # get entries from POST request
            first_name = request.POST.get("first_name", "")
            last_name = request.POST.get("last_name", "")
            motto = request.POST.get("motto", "")
            about = request.POST.get("about", "")

            u.first_name = first_name
            u.last_name = last_name
            u.save()

            # try to create it
            try:
                user_details = UserDetails.objects.get(user=u)
                user_details.title = motto
                user_details.about = about
                user_details.save()
            except UserDetails.DoesNotExist:
                user_details = UserDetails.objects.create(user=u, slug = slugify(motto), title = motto,  about = about)

            # notification
            notification = "<strong>Sukces!</strong> Informacje o użytkowniku zostału zaktualizwoane"
            return render_to_response('dashboard/user_settings.html',
                { 'first_name' : u.first_name, 'last_name' : u.last_name,
                'about' : user_details.about, 'motto' : user_details.title,
                'notification' : notification,
                'background_image' : user_details.background_image,
                'publisherNews': publisherNews
                }, context_instance=RequestContext(request))

        #not used now
        elif "avatar_image" in request.POST:
            # TODO avatar image
            # upload file
            # change in model UserDetails
            image = request.POST.get("avatar_file", "")
            print(request.POST)

            try:
                user_details = UserDetails.objects.get(user=u)
                user_details.icon = image
                user_details.save()
                notification = "<strong>Sukces!</strong> Awatar został zmieniony"
            except UserDetails.DoesNotExist:
                user_details = UserDetails.objects.create(user=u, slug = slugify(motto), title = motto,  about = about, icon = image)

            if u.first_name :
                try:
                    user_details = UserDetails.objects.get(user=u) # get UserDetails object from User object
                    return render_to_response('dashboard/user_settings.html', {
                        "first_name" : u.first_name, "last_name" : u.last_name,
                        "about":user_details.about, "motto":user_details.title,
                        "notification":notification, 'publisherNews':publisherNews
                        }, context_instance=RequestContext(request))
                except UserDetails.DoesNotExist:
                    return render_to_response('dashboard/user_settings.html', {
                        'first_name' : u.first_name, "last_name" : u.last_name,
                        'publisherNews':publisherNews
                        }, context_instance=RequestContext(request))
            else:
                return render_to_response('dashboard/user_settings.html', {  }, context_instance=RequestContext(request))

        elif "background_image" in request.POST:
            # TODO background image
            # upload file
            # change in model UserDetails
            background_image = request.POST.get("background_image", "")
            try:
                user_details = UserDetails.objects.get(user=u)
                user_details.background_image = background_image
                user_details.save()
            except UserDetails.DoesNotExist:
                user_details = UserDetails.objects.create(user=u, background_image=background_image)

            notification = "<strong>Sukces!</strong> Zdjęcie w tle zostało zaktualizowane"

            return render_to_response('dashboard/user_settings.html',
                { "first_name" : u.first_name, "last_name" : u.last_name,
                "about":user_details.about, "motto":user_details.title,
                "notification":notification , "background_image":user_details.background_image,
                'publisherNews':publisherNews
                }, context_instance=RequestContext(request))
    else: # check user isn't loged -> return to main
        return render_to_response('index.html', {}, context_instance=RequestContext(request))


def dashboard_change_password(request):
    if request.method == 'GET': # handling GET HTTP request
        return render_to_response('dashboard/change_password.html', {}, context_instance=RequestContext(request))
    elif request.method == 'POST': # handling POST HTTP request
        if "password_first" in request.POST:
            password = request.POST.get("password_first", "")
            password2 = request.POST.get("password_second", "")

            print(password)
            print(password2)

            if password == password2:
                password_hash = hashlib.md5(password).hexdigest()
                u = request.user
                u.password = password_hash
                u.save()
                notification = "<strong>Haslo</strong> zostalo zmienione ;)"
            else:
                notification = "<strong>hasla</strong> nie sa identyczne ;)"

            return render_to_response('dashboard/change_password.html',
                {"notification":notification}, context_instance=RequestContext(request))
    else:
        return render_to_response('index.html', {}, context_instance=RequestContext(request))


def upload_image(request):
    '''Simple view method for uploading an image'''
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid() and form.is_multipart():
            save_file(request.FILES['image'])
            return HttpResponse('Thanks for uploading the image')
        else:
            return HttpResponse('Invalid image')
    else:
        form = ImageForm()
        return render_to_response('sample/upload_image_form.html', {'form': form})

def save_file(file, path=''):
    ''' Little helper to save a file'''
    filename = file._get_name()
    fd = open('%s/%s' % (MEDIA_ROOT, str(path) + str(filename)), 'wb')

    for chunk in file.chunks():
        fd.write(chunk)

    fd.close()
