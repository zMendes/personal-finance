from django.db import models
from django.utils.timezone import now


class User(models.Model):
    name = models.CharField(max_length=25, primary_key=True)


class Item(models.Model):

    ACCOUNT_CHOICES = {
        'joint': 'joint',
        'leo':'leo',
        'tchel': 'tchel'
    }
    PAYMENT = {
        'debit':'debit',
        'credit':'credit',
        'VR': 'vr'
    }
    description = models.CharField(max_length=200)
    date = models.DateTimeField(default=now)
    item_user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.CharField(choices=ACCOUNT_CHOICES, max_length=8)
    payment_type = models.CharField(choices=PAYMENT, max_length=8)
    value = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['date', 'item_user', 'value', 'description'], name='unique_migration_host_combination'
            )
        ]