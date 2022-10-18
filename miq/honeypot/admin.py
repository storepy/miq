from django.contrib import admin

from .models import Attempt


@admin.register(Attempt)
class LoginAdmin(admin.ModelAdmin):
    model = Attempt
    list_display = ['username', 'password', 'ip', 'path', 'payload']
