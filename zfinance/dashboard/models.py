from django.db import models
from django.utils.timezone import now


class User(models.Model):
    name = models.CharField(max_length=25)


class Item(models.Model):

    ACCOUNT_CHOICES = {
        'JOINT': 'joint',
        'LEO':'leo',
        'TCHEL': 'tchel'
    }
    PAYMENT = {
        'debit':'debit',
        'credit':'credit'
    }
    description = models.CharField(max_length=200)
    date = models.DateTimeField(default=now)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.CharField(choices=ACCOUNT_CHOICES, max_length=8)
    payment_type = models.CharField(choices=PAYMENT, max_length=8)
    value = models.IntegerField()