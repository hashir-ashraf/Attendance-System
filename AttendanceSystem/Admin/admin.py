from django.contrib import admin
from .models import CustomUser
# Register your models here.
admin.site.register(CustomUser)
from .models import Profile

admin.site.register(Profile)
