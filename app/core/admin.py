from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AccountModel

admin.site.register(AccountModel, UserAdmin)