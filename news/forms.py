# -*- coding: utf-8 -*-

from django import forms
import django.contrib.auth
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
import re

class FormularzRejestracji(forms.Form):
   username = forms.CharField(label="Login:",max_length=30)
   email = forms.EmailField(label="Email:")
   password1 = forms.CharField(label="Hasło:",widget=forms.PasswordInput())
   password2 = forms.CharField(label="Powtorz hasło:",widget=forms.PasswordInput())
   # phone = forms.CharField(label="Telefon:",max_length=20,required=False)
   log_on = forms.BooleanField(label="Logowanie po rejestracji:",required=False)

   def clean_password2(self):
      password1=self.cleaned_data['password1']
      password2=self.cleaned_data['password2']
      if password1==password2:
         return password2
      else:
         raise forms.ValidationError("Hasła nie są takie same")

   def clean_username(self):
      username = self.cleaned_data['username']
      if not re.search(r'^\w+$',username):
         raise forms.ValidationError("Dopuszczalne sa tylko cyfry, litery angielskie i  znak \"_\" ")

      try:
         User.objects.get(username=username)
      except ObjectDoesNotExist:
         return username
      raise forms.ValidationError("Taki użytkownik już istnieje")
