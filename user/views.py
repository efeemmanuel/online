from multiprocessing import context
from django.shortcuts import redirect, render,get_list_or_404, get_object_or_404,reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from .models import *
from index.forms import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage,EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.encoding import force_text  # Use this import for Django versions prior to 4.0

from .utils import generate_token
import threading
import string
import random
from django.contrib.auth.decorators import user_passes_test


User = get_user_model()

class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def send_activation_email(user, request):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('acc/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMultiAlternatives(subject=email_subject, body=email_body, from_email=settings.EMAIL_HOST_USER,to=[user.email] )
    email.attach_alternative(email_body, "text/html")

    EmailThread(email).start()


@login_required(login_url='/user/login/')
def profile(request):
    qs = Withdraw.objects.filter(user=request.user)
    qs1 = crypto.objects.filter(user=request.user)
    context = {'qs':qs,'cry':qs1}
    return render(request, 'acc/dash.html',context)

@login_required(login_url='/user/login/')
def loan(request):
    if request.method == "POST":
        pur = request.POST.get('pur')
        price = request.POST.get('amm')
        credit = request.POST.get('credit')
        ten = request.POST.get('ten')
        if float(price) > float(request.user.avaliablebalance):
            messages.error(request, 'Insufficient Funds')
        else:
            user = User.objects.get(username=request.user)
            cre = Loan(pur=pur,ammount=price,credit=credit,ten=ten,user=user)
            cre.save()
            messages.error(request, 'Loan Pending...')
    return render(request, 'acc/loan.html')

@login_required(login_url='/user/login/')
def card(request):
    return render(request, 'acc/card.html')

@login_required(login_url='/user/login/')
def mysum(request):
    qs = Withdraw.objects.filter(user=request.user)
    context = {'qs':qs}
    return render(request, 'acc/sum.html',context)

@login_required(login_url='/user/login/')
def withdrawal(request):
    if request.method == "POST":
        accountname = request.POST.get('accountname')
        accountnumber = request.POST.get('accountnumber')
        bankname = request.POST.get('bankname')
        ibancode = request.POST.get('iban')
        swiftcode = request.POST.get('swift')
        country = request.POST.get('con')
        state = request.POST.get('state')
        description = request.POST.get('des')
        bankaddress = request.POST.get('bankad')
        amount = request.POST.get('ammount')
        email = request.POST.get('email')
        user = User.objects.get(username=request.user)
        checkactive = user.withdraw
        if float(amount) > float(request.user.avaliablebalance):
            messages.error(request, 'Insufficient Funds')
        elif checkactive == True:
            return redirect('userurl:otp')
        else:
            newamount = int(request.user.avaliablebalance) - int(amount)
            user.avaliablebalance = int(newamount)
            user.save()
            cre = Withdraw.objects.create(accountname=accountname,accountnumber=accountnumber,bankname=bankname,amount=amount,user=user,ibancode=ibancode,swiftcode=swiftcode,bankaddress=bankaddress,country=country,state=state,description=description)
            email_body = render_to_string('acc/mali.html', {
            'data':cre,
            'user':user
            })
            msg = EmailMultiAlternatives(subject='Receipt', body=email_body, from_email=settings.DEFAULT_FROM_EMAIL,to=[email] )
            msg.attach_alternative(email_body, "text/html")
            msg.send()
            user.withdraw = True
            user.save()
        return redirect('userurl:pin')
    return render(request, 'acc/cross.html')

def otp(request):
    return render(request,'acc/bad.html')


# @login_required(login_url='/user/login/')
# def pay(request,slug):
#     post = get_object_or_404(Pay_method, slug=slug)
#     if request.method == 'POST':
#         image = request.FILES.get('image')
#         user = User.objects.get(username=request.user)
#         cre = Payment(image=image,user=user)
#         cre.save()
#         return render(request, 'acc/suc1.html')
#     context = {'data':post}
#     return render(request, 'acc/fund.html',context)
@login_required(login_url='/user/login/')
def pay(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        user = User.objects.get(username=request.user)
        cre = Che(image=image,user=user)
        cre.save()
        messages.success(request,'Your Payment will be Aproved in the next 24hrs...')
    context = {'data':pay}
    return render(request, 'acc/depo.html',context)

def fund(request):
    qs = Pay_method.objects.filter()
    context = {'wal':qs}
    return render(request, 'acc/depo.html',context)

def loca(request):
    if request.method == "POST":
        accountnumber = request.POST.get('accountnumber')
        price = request.POST.get('ammount')
        ibancode = request.POST.get('iban')
        swiftcode = request.POST.get('swift')
        if float(price) > float(request.user.avaliablebalance):
            messages.error(request, 'Insufficient Funds')
        else:
            user = User.objects.get(username=request.user)
            newamount = int(request.user.avaliablebalance) - int(price)
            user.avaliablebalance = int(newamount)
            user.save()
            cre = Local_trans(accountnumber=accountnumber,amount=price,user=user,ibancode=ibancode,swiftcode=swiftcode)
            cre.save()
            return redirect('userurl:pin')
    return render(request,'acc/loca.html')


def signupView(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return redirect('userurl:signup')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match')
            return redirect('userurl:signup')
        else:
            randompin = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(15))
            user = User.objects.create_user(username=username, password=password1,email=email,accnumber=randompin)
            return redirect('userurl:login')
    return render(request, 'newhome/signup.html')

def loginView(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            newurl = request.GET.get('next')
            if newurl:
                return redirect(newurl)
            return redirect('userurl:profile')
        else:
            messages.error(request, 'Invalid Credentials')
    context = {}
    return render(request, 'newhome/login.html')

def logout_view(request):
	logout(request)
	return redirect('/user/login')

def activate_user(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()

        messages.add_message(request, messages.SUCCESS,'Email verified, you can now login')
        return redirect('userurl:login')

    return render(request, 'acc/activate-failed.html', {"user": user})



def pin(request):
    if request.method == 'POST':
        pin = request.POST.get('pin')
        try:
            loadedpin = Pin.objects.get(pin=pin)
            checkactive = loadedpin.active
            if checkactive == True:
                messages.error(request, 'Pin already in use')
            else:
                loadedpin.active = True
                loadedpin.save()
                text = 'Pin Successfully Loaded'
                context = {'text':text}
                return render(request, 'acc/suc1.html', context)
        except Pin.DoesNotExist:
            messages.error(request, 'Invalid Pin')
    return render(request,'acc/pin.html')

def cry(request):
    if request.method == "POST":
        wallet = request.POST.get('wal')
        price = request.POST.get('ammount')
        coin = request.POST.get('coin')
        user = User.objects.get(username=request.user)
        checkactive = user.withdraw
        if float(price) > float(request.user.avaliablebalance):
            messages.error(request, 'Insufficient Funds')
        elif checkactive == True:
            return redirect('userurl:otp')
        else:
            user = User.objects.get(username=request.user)
            newamount = int(request.user.avaliablebalance) - int(price)
            user.avaliablebalance = int(newamount)
            user.save()
            cre = crypto(wallet=wallet,amount=price,user=user,coin=coin,)
            cre.save()
            user.withdraw = True
            user.save()
            return redirect('userurl:pin')
    return render(request,'acc/wal.html')


def mywith(request,id):
    post = get_object_or_404(Withdraw, id=id)
    context = {'data':post}
    return render(request,'acc/trans.html',context)

def myveri(request):
    if request.method == "POST":
        num = request.POST.get('ssn')
        phone = request.POST.get('phone')
        image1 = request.FILES.get('image1')  # Update to 'image1'
        image2 = request.FILES.get('image2')  # Add this line
        cre = Veri.objects.create(ssn=num,phone=phone,image1=image1,image2=image2)
        messages.error(request, 'Verification Under review....')
    return render(request, 'acc/kyc.html')