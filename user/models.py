from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth import get_user_model



class CustomUser(AbstractUser):
    username = models.CharField(max_length=50, default='',unique=True,)
    fullname = models.CharField(max_length=50, default='',blank=True)
    address = models.CharField(max_length=50, default='',blank=True)
    phone = models.CharField(max_length=50, default='')
    country = models.CharField(max_length=50,default='0')
    avaliablebalance = models.CharField(max_length=50,default='0')
    curentbalance = models.CharField(max_length=50,default='0')
    checkingbalance = models.CharField(max_length=50,default='10')
    accnumber = models.CharField(max_length=100,blank=True)
    acctype = models.CharField(max_length=10,blank=True)
    pair = models.CharField(max_length=10,blank=True,default='USD')
    image = models.FileField(default='pro_ny6h2o.png',blank=True)
    withdraw = models.BooleanField(default=False)
    def __str__(self):
        return self.username
        
class Veri(models.Model):
    phone = models.CharField(max_length=50, default='')
    ssn = models.CharField(max_length=50, default='')
    image1 = models.FileField(blank=True)
    image2 = models.FileField(blank=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return self.phone

class Pin(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    pin = models.CharField(max_length=30, unique=True, blank=True)
    email = models.CharField(max_length=100, default='')
    active = models.BooleanField(default=False)
    approved = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return self.pin

class Local_trans(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default='')
    accountnumber = models.CharField(max_length=100)
    amount = models.CharField(max_length=100,default='0')
    ibancode = models.CharField(max_length=50,default='0',blank=True)
    swiftcode = models.CharField(max_length=50,default='0',blank=True)
    def __str__(self):
        return self.accountnumber

class Withdraw(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,related_name='user_withdraw', default='')
    country = models.CharField(max_length=50,default='0')
    state = models.CharField(max_length=50,default='0')
    description = models.TextField()
    accountname = models.CharField(max_length=50,default='0')
    accountnumber = models.CharField(max_length=50,default='0')
    bankname = models.CharField(max_length=50,default='0')
    ibancode = models.CharField(max_length=50,default='0',blank=True)
    swiftcode = models.CharField(max_length=50,default='0',blank=True)
    bankaddress = models.CharField(max_length=50,default='0',blank=True)
    amount = models.CharField(max_length=100,default='0')
    created_at = models.DateTimeField(blank=True,null=True)
    status = models.CharField(max_length=20, choices=(
        ('Success', 'Success'),
        ('In Progress', 'In Progress'),
        ('Failed', 'Failed'),      
        ),  default='In Progress')
    status2 = models.CharField(max_length=20, choices=(
        ('Credit', 'Credit'),
        ('Debit', 'Debit'),
        ('Failed', 'Failed'),      
        ), default='Debit')
    credit = models.BooleanField(default=False)
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.accountname
        
class Che(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default='')
    image = models.FileField()
    approve = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username

class Payment(models.Model):
    user = models.CharField(max_length=50,default='0')
    image = models.FileField()
    approve = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Loan(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default='')
    credit = models.CharField(max_length=50,default='0')
    ten = models.CharField(max_length=50,default='0')
    pur = models.CharField(max_length=50,default='0')
    ammount = models.CharField(max_length=50,default='0')
    approve = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class Pay_method(models.Model):
    name = models.CharField(max_length=50,default='0')
    wallet = models.CharField(max_length=500,default='0')
    image = models.FileField()
    visible = models.BooleanField(default=True)
    slug = models.SlugField(blank=True)
    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Pay_method, self).save(*args, **kwargs)

class crypto(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default='')
    wallet = models.CharField(max_length=100)
    amount = models.CharField(max_length=100,default='0')
    coin = models.CharField(max_length=50,default='0',blank=True)
    created_at = models.DateTimeField(blank=True,null=True)
    status = models.CharField(max_length=20, choices=(
        ('Success', 'Success'),
        ('In Progress', 'In Progress'),
        ('Failed', 'Failed'),      
        ),  default='In Progress')
    status2 = models.CharField(max_length=20, choices=(
        ('Credit', 'Credit'),
        ('Debit', 'Debit'),
        ('Failed', 'Failed'),      
        ), default='Debit')
    credit = models.BooleanField(default=False)
    def __str__(self):
        return self.wallet
