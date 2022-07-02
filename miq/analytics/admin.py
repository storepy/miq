from django.contrib import admin

from .models import Hit, SearchTerm


class HitModelAdmin(admin.ModelAdmin):
    list_display = (
        'path', 'method', 'source_id', 'session', 'ip',
        'referrer', 'response_status', 'user_agent', 'debug', 'url', 'slug',
    )


admin.site.register(Hit, HitModelAdmin)


class SearchTermModelAdmin(admin.ModelAdmin):
    list_display = ('value', 'count', 'session', 'slug',)


admin.site.register(SearchTerm, SearchTermModelAdmin)
