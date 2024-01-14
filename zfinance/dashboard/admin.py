from django.contrib import admin
from .models import User, Movement, Account

# Register your models here.
admin.site.register(User)
admin.site.register(Movement)
admin.site.register(Account)
