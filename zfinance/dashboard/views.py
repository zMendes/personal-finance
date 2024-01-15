from django.http import HttpResponse
from dashboard.models import User, Account, Movement
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, render
from django.core import serializers
import json


def index(request):
    movements_by_month_year = Movement.objects.values_list("date", flat=True).distinct()
    months = [x.strftime("%B") for x in movements_by_month_year]
    years = [x.strftime("%Y") for x in movements_by_month_year]

    return render(request, "home.html", {"months": months, "years": years})


def get_movement_from_month_year(request, year, month):
    from datetime import datetime

    datetime_obj = datetime.strptime(f"{month} {year}", "%B %Y")
    movement_list = Movement.objects.filter(
        date__year=year, date__month=datetime_obj.month
    )
    data = serializers.serialize("json", movement_list)

    return HttpResponse(data, content_type="application/json")


@csrf_exempt
def add_movement(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        transaction_type = data["type"]
        match transaction_type:
            case "expenses":
                return process_expense(data)
            case "investment":
                return move_to_investment(data)
            case "transfer_out":
                return transfer_money(data)
            case "credit_card_bill":
                return pay_credit_bill(data)
            case "salary":
                return give_salary(data)
            case "transfer_in":
                return add_money(data)


def add_money(data):
    user = User.objects.get(name=data["user"])
    account = Account.objects.get(owner=data["account"])
    movement = Movement(
        movement_user=user,
        account_user=account,
        transaction_type=data["type"],
        value=data["value"],
    )
    account.balance += data["value"]
    movement.save()
    account.save()
    return HttpResponse("Success. UwU")


def process_expense(data):
    user = User.objects.get(name=data["user"])
    account = Account.objects.get(owner=data["account"])
    payment_type = data["payment"]
    value = data["value"]
    movement = Movement(
        description=data["description"],
        movement_user=user,
        account_user=account,
        payment_type=payment_type,
        transaction_type=data["type"],
        value=data["value"],
    )
    if payment_type == "credit":
        account.credit_bill += value
    else:
        account.balance -= value
    movement.save()
    account.save()
    return HttpResponse("Success. UwU")


def transfer_money(data):
    user = User.objects.get(name=data["user"])
    account = Account.objects.get(owner=data["account"])
    target_account = Account.objects.get(owner=data["target_account"])
    movement = Movement(
        description=f"Transfer to {target_account}",
        movement_user=user,
        account_user=account,
        transaction_type="transfer_out",
        to=target_account,
        value=data["value"],
    )
    account.balance -= data["value"]
    target_account.balance += data["value"]
    movement.save()
    account.save()
    target_account.save()
    return HttpResponse("Success. UwU")


def move_to_investment(data):
    user = User.objects.get(name=data["user"])
    account = Account.objects.get(owner=data["account"])
    movement = Movement(
        description=f"Investment",
        movement_user=user,
        account_user=account,
        transaction_type="investment",
        value=data["value"],
    )
    account.balance -= data["value"]
    account.investments += data["value"]
    movement.save()
    account.save()
    return HttpResponse("Success. UwU")


def pay_credit_bill(data):
    return HttpResponse("Success. UwU")


def give_salary(data):
    return HttpResponse("Success. UwU")
