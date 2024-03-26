from django.contrib.auth import get_user_model
from django import forms
from .models import *

User = get_user_model()


# class ProfileUpdateForm(forms.ModelForm):

# 	class Meta:
# 		model = User
# 		fields = ['username','first_name','last_name','fullname','address','country','phone','image','name_oncard','cardnumber','cvc','exp','postal','ssn','street','city','id1','id2',]

