from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator


class User(models.Model):
    name = models.CharField(max_length=25, primary_key=True)

    def __str__(self):
        return f"{self.name}"


class Account(models.Model):
    ACCOUNT_CHOICES = {
        "joint": "joint",
        "leo": "leo",
        "tchel": "tchel",
        "vr-leo": "vr-leo",
        "vr-tchel": "vr-tchel",
    }
    owner = models.CharField(choices=ACCOUNT_CHOICES, max_length=8, primary_key=True)
    balance = models.FloatField()
    investments = models.FloatField(default=0)
    credit_bill = models.FloatField(default=0)
    salary_date = models.IntegerField(validators=[MaxValueValidator(31)])

    def __str__(self):
        return f"{self.owner}"


class Movement(models.Model):
    PAYMENT = {"debit": "debit", "credit": "credit", "VR": "vr"}
    MOVEMENT_TYPE = {
        "investment": "investment",
        "transfer": "transfer",
        "expenses": "expenses",
        "credit_card_bill": "credit_card_bill",
        "salary": "salary",
        "add": "add",
    }
    description = models.CharField(max_length=200)
    date = models.DateTimeField(default=now)
    movement_user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_user = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="original_account"
    )
    payment_type = models.CharField(choices=PAYMENT, max_length=8)
    to = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="target_account",
        null=True,
        default=None,
    )
    transaction_type = models.CharField(choices=MOVEMENT_TYPE, max_length=16)
    value = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["date", "movement_user", "value", "description"],
                name="unique_migration_host_combination",
            )
        ]

    def __str__(self):
        return f"{self.description}, {self.value} - {self.item_user}"
