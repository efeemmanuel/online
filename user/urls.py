from django.urls import path
from . import views
from .views import *
app_name='userurl'
urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signupView, name='signup'),
    path('login/', views.loginView, name='login'),
   
    path('logout/', views.logout_view, name='logout'),
   
    path('withdrawal/', views.withdrawal, name='withdraw'),
    path('fund/', views.pay, name='fund'),
    path('deposit/', views.fund, name='depo'),
    path('Account-summary/', views.mysum, name='sum'),
    path('receipt/<id>/', views.mywith, name='receipt'),
    
    path('error-transfer/', views.otp,name='otp'),
    path('loan/', views.loan,name='loan'),
    path('cards/', views.card,name='card'),
    path('pin/', views.pin,name='pin'),
    path('local-transfer/', views.loca,name='loca'),
    path('crypto-transfer/', views.cry,name='cry'),
    path('verify/', views.myveri,name='veri'),
    path('activate-user/<uidb64>/<token>', views.activate_user, name='activate'),
       
]