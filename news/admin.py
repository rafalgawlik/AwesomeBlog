# -*- coding: utf-8 -*-
from django.contrib import admin
from news.models import *

'''
File: admin.py
Author: Rafal Gawlik
Description: admin page
Created: 13.11.2014 Wroclaw
'''

class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ('title', 'user')
    prepopulated_fields = {'slug': ('title',)}


class BlogAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    prepopulated_fields = {'slug': ('name',)}


class TagAdmin(admin.ModelAdmin):
    list_display = ('name','icon')
    prepopulated_fields = {'slug': ('name',)}


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    prepopulated_fields = {'slug': ('name',)}


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_date')
    prepopulated_fields = {'slug': ('title',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'posted_date')
    prepopulated_fields = {'slug': ('text',)}


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('text', 'posted_date')
    prepopulated_fields = {'slug': ('text',)}


class PublisherNewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_date')
    prepopulated_fields = {'slug': ('title',)}


admin.site.register(UserDetails, UserDetailsAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(PublisherNews, PublisherNewsAdmin)
