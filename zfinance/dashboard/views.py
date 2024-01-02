from django.http import HttpResponse
from dashboard.models import User


def index(request):
    return HttpResponse("Hello, world. You're at the dashboard index.")

def add_entry(request):
    pass