from django.urls import path
from . import views

app_name = 'indexurl'
urlpatterns = [
	path('', views.myindex, name='index'),
	path('contact/',  views.mycontact ,name='contact'),
	path('about-us/',  views.myabout ,name='about'),
	path('privacy_policy/',  views.myprivate ,name='private'),
	path('services/',  views.services_view ,name='services'),
	path('loan/',  views.loan_view ,name='loan'),
	
	
]

 