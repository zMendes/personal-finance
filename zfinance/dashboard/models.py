from django.db import models
from django.utils.timezone import now


class User(models.Model):
    name = models.CharField(max_length=25, primary_key=True)
    def __str__(self):
        return f'{self.name}'

class Account(models.Model):

    ACCOUNT_CHOICES = {
            'joint': 'joint',
            'leo':'leo',
            'tchel': 'tchel'
        }
    owner = models.CharField(choices=ACCOUNT_CHOICES, max_length=8, primary_key=True)
    balance = models.FloatField()
    investments = models.FloatField()
    
    def __str__(self):
        return f'{self.owner}'

class Item(models.Model):

    PAYMENT = {
        'debit':'debit',
        'credit':'credit',
        'VR': 'vr'
    }
    description = models.CharField(max_length=200)
    date = models.DateTimeField(default=now)
    item_user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_type = models.CharField(choices=PAYMENT, max_length=8)
    value = models.FloatField()
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['date', 'item_user', 'value', 'description'], name='unique_migration_host_combination'
            )
        ]
    def __str__(self):
        return f'{self.description}, {self.value} - {self.item_user}'
