from django.contrib.auth.models import User
from django.db import models

'''
File: models.pl
Author: Rafal Gawlik
Description: File content models used in app
Created: 13.11.2014 Wroclaw

UserDetails
Blog
Tag
Category
Category
News
Comment
Notification
PublisherNews
'''

class UserDetails(models.Model):
   """
   UserDetails
   Extend User model
   """
   title = models.CharField('Motto', max_length=255)
   slug = models.SlugField('Slug', max_length=255, unique=True)
   user = models.ForeignKey(User)
   about = models.TextField(verbose_name='Content')
   icon = models.ImageField('Icon', upload_to='icons', blank=True)
   background_image = models.CharField('Background image', max_length=255)

   class Meta:
      verbose_name = "UserDetails"
      verbose_name_plural = "UserDetails"

   def __unicode__(self):
      return self.title


class Blog(models.Model):
   """Blog"""
   name = models.CharField('Name', max_length=100)
   slug = models.SlugField('Slug', unique=True, max_length=100)
   date_created = models.DateTimeField('Date', auto_now_add=True)
   description = models.TextField(verbose_name='Description')
   user = models.ForeignKey(User)
   background_image = models.CharField('Background image', max_length=255)
   comment_moderate = models.BooleanField('Comment moderate', default=True) # True if should be moderated

   class Meta:
      verbose_name = "Blog"
      verbose_name_plural = "Blogs"

   def __unicode__(self):
      return self.name


class Tag(models.Model):
   """Tag for blog post, object have entries about tag entry"""
   name = models.CharField('Name', max_length=100)
   slug = models.SlugField('Slug', unique=True, max_length=100)
   icon = models.ImageField('Icon', upload_to='icons',blank=True)

   class Meta:
      verbose_name = "Tag"
      verbose_name_plural = "Tags"

   def __unicode__(self):
      return self.name


class Category(models.Model):
   """Post category, object have post category entries"""
   name = models.CharField(max_length=128, unique=True)
   slug = models.SlugField('Slug', unique=True, max_length=100)
   icon = models.ImageField('Icon', upload_to='icons',blank=True)

   class Meta:
      verbose_name = "Category"
      verbose_name_plural = "Category"

   def __unicode__(self):
      return self.name


class News(models.Model):
   """Blog news model, object have blog post entries"""
   title = models.CharField('Title', max_length=255)
   slug = models.SlugField('Slug', max_length=255, unique=True)
   description = models.TextField(verbose_name='Description', default=None, null=True, blank=True)
   text = models.TextField(verbose_name='Content', default=None, null=True, blank=True)
   draft = models.BooleanField('Draft', default=False)
   blog = models.ForeignKey(Blog)
   #category = models.ForeignKey(Category, default=None, null=True, blank=True)
   tags = models.ManyToManyField(Tag, verbose_name='Tags', default=None, null=True, blank=True)
   posted_date = models.DateTimeField('Date', auto_now_add=True)
   status = models.BooleanField('Publsihed', default=True) # True if accepted

   class Meta:
      verbose_name = "News"
      verbose_name_plural = "News"

   def __unicode__(self):
      return self.title

class Comment(models.Model):
   """Comment for post"""
   text =  models.CharField('Text', max_length=255)
   slug = models.SlugField('Slug', max_length=255, unique=True)
   user = models.ForeignKey(User)
   news = models.ForeignKey(News)
   posted_date = models.DateTimeField('Date', auto_now_add=True)
   status = models.BooleanField('Accetped', default=False) # True if accepted

   class Meta:
      verbose_name = "Comment"
      verbose_name_plural = "Comments"

   def __unicode__(self):
      return self.text


class Notification(models.Model):
   """Notification for user notifiction panel"""
   text = models.CharField('Text', max_length=255)
   slug = models.SlugField('Slug', max_length=255, unique=True)
   type = models.CharField('Type', max_length=255)
   posted_date = models.DateTimeField('Date', auto_now_add=True)
   user = models.ForeignKey(User)

   class Meta:
      verbose_name = "Notification"
      verbose_name_plural = "Notifications"

   def __unicode__(self):
      return self.text


class PublisherNews(models.Model):
    """Publisher News - informtion panel with content from platform admin"""
    title = models.CharField('Title', max_length=255)
    slug = models.SlugField('Slug', max_length=255, unique=True)
    description = models.TextField(verbose_name='Description', default=None, null=True, blank=True)
    posted_date = models.DateTimeField('Date', auto_now_add=True)

    class Meta:
        verbose_name = "PublisherNews"
        verbose_name_plural = "PublisherNews"

    def __unicode__(self):
        return self.title
