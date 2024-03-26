from django.contrib import admin
from .models import *



class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username',  'email']
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user',  'approve']
class PinAdmin(admin.ModelAdmin):
    list_display = ['pin','user',  'active','time']

admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Withdraw)
admin.site.register(Pin,PinAdmin)
admin.site.register(Local_trans)
admin.site.register(Pay_method)
admin.site.register(crypto)
admin.site.register(Loan)
admin.site.register(Che)
admin.site.register(Veri)

admin.site.register(Payment,PaymentAdmin)