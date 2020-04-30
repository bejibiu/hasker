from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Account


class UserInline(admin.StackedInline):
    model = Account
    can_delete = False


class UserWithAvatar(UserAdmin):
    inlines = (UserInline,)


admin.site.unregister(User)
admin.site.register(User, UserWithAvatar)
