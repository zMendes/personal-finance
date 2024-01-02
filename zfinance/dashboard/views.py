from django.http import HttpResponse
from dashboard.models import User


def index(request):
    return HttpResponse("Hello, world. You're at the dashboard index.")

def create_user(request):
    users = User.objects.all()
    for user in users:
        print(user.name)
    return HttpResponse("User created!")
