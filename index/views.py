from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.contrib import messages
from django.http import HttpResponse, request


def myindex(request):
    qs = Review.objects.all()
    context = {'rev':qs}
    return render(request, 'newhome/home.html',context)


def mycontact(request):
	if request.method == 'POST':
		form = Contactform(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Thanks for your message we will reply you shortly')
			
	else:
		form = Contactform()
	return render(request, 'newhome/contact.html')


def myabout(request):
	return render(request, 'newhome/about.html')


def services_view(request):
	return render(request, 'newhome/card.html')

def loan_view(request):
	return render(request, 'newhome/loan.html')

def myprivate(request):
	return render(request, 'newhome/privacy-policy.html')