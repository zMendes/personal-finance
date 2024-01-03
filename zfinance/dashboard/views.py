from django.http import HttpResponse
from dashboard.models import User, Item
from django.views.decorators.csrf import csrf_exempt
import json


def index(request):
    return HttpResponse("Hello, world. You're at the dashboard index.")

@csrf_exempt
def insert_item(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        user = User.objects.get(name=data['user'])
        item = Item(
            description = data['description'],
            item_user = user,
            account = data['account'],
            payment_type = data['payment'],
            value = data['value']
        )
        item.save()
    return HttpResponse("Success. UwU")