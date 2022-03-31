from django.contrib import admin

from .models import Hit


class HitModelAdmin(admin.ModelAdmin):
    list_display = ('slug', 'source')


admin.site.register(Hit, HitModelAdmin)
