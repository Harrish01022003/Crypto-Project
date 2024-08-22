from django.contrib import admin
from .models import Transaction, TwoFactorAuth

admin.site.register(Transaction)
admin.site.register(TwoFactorAuth)
