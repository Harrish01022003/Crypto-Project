from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reciever = models.CharField(max_length=255, default='None')
    status = models.CharField(max_length=20, blank=True, default='Failed')

    def __str__(self):
        return self.user.username

class TwoFactorAuth(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    vein_pattern = models.FileField(upload_to='vein')

    def __str__(self):
        return self.user.username
