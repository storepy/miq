from django.contrib import admin

from .models import Hit, LIB, Visitor, Bot


class HitModelAdmin(admin.ModelAdmin):
    list_display = (
        'path', 'method', 'source_id', 'session', 'ip',
        'referrer', 'response_status', 'user_agent', 'debug', 'url', 'slug',
    )


admin.site.register(Hit, HitModelAdmin)


class LIBModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'utm_medium', 'utm_source', 'utm_content', 'is_pinned')


admin.site.register(LIB, LIBModelAdmin)


admin.site.register(Visitor)
admin.site.register(Bot)
