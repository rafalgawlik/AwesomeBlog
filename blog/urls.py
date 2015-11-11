from django.conf.urls import patterns, include, url
from django.contrib import admin

'''
File: urls.pl
Author: Rafal Gawlik
Description: File content url regexp
Created: 13.11.2014 Wroclaw
'''

admin.autodiscover()

urlpatterns = patterns('',
   url(r'^admin/*', include(admin.site.urls)),
   url(r'^/?$', 'news.views.index'), # index main
   url(r'^login/*$','django.contrib.auth.views.login'), #login
   url(r'^logout/*$','news.views.logout_page'), #logout
   url(r'^register/*$','news.views.register_page'), #register
   url(r'^user/(?P<slug>[\w\-_]+)$','news.views.user'), #user

   url(r'^dashboard/*$','news.views.dashboard'), #dashboard

   url(r'^dashboard/blogs/*$','news.views.dashboard_blogs'), #dashboard/blogs
   url(r'^dashboard/blogs/(?P<slug>[\w\-_]+)*$','news.views.dashboard_blog_post'), #dashboard/blogs - configuration link and post list
   url(r'^dashboard/blogs/(?P<slug>[\w\-_]+)/configuration*$','news.views.dashboard_blogs_configuration'), #dashboard/blogs - blog configuration
   url(r'^dashboard/blogs/(?P<slug>[\w\-_]+)/delete*$','news.views.dashboard_blogs_delete'), #dashboard/blogs - blog configuration

   url(r'^dashboard/post/(?P<slug>[\w\-_]+)*$','news.views.dashboard_post'), #dashboard/post - post editor
   url(r'^dashboard/post/(?P<slug>[\w\-_]+)/delete*$','news.views.dashboard_post_delete'), #dashboard/dete post

   url(r'^dashboard/comments/*$','news.views.dashboard_comments'), #dashboard/blogs
   url(r'^dashboard/comments/(?P<slug>[\w\-_]+)*$','news.views.dashboard_comments_blog'), #dashboard/blogs
   url(r'^dashboard/comments/(?P<slug_blog>[\w\-_]+)/(?P<slug_post>[\w\-_]+)/?$','news.views.dashboard_comments_post'), #dashboard/blogs

   url(r'^dashboard/usersettings/*$','news.views.dashboard_user_settings'), #dashboard/blogs
   url(r'^dashboard/change-password/*$','news.views.dashboard_change_password'), #dashboard/change_password

   url(r'^(?P<slug>[\w\-_]+)/?$', 'news.views.blog'), #blog main page
   url(r'^(?P<slug>[\w\-_]+)/(?P<id>[0-9]+)/$', 'news.views.post'), #post view
)
