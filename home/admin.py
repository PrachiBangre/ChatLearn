from django.contrib import admin

# Register your models here.
from.models import SignUp
from.models import SignIn

admin.site.register(SignIn)
admin.site.register(SignUp)