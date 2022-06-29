from django.contrib import admin

from .models import Hit, SearchTerm


class HitModelAdmin(admin.ModelAdmin):
    list_display = ('path', 'source_id', 'ip', 'method', 'response_status', 'debug', 'url', 'slug',)


admin.site.register(Hit, HitModelAdmin)


class SearchTermModelAdmin(admin.ModelAdmin):
    list_display = ('value', 'count', 'session', 'slug',)


admin.site.register(SearchTerm, SearchTermModelAdmin)
