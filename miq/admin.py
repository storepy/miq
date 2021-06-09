from django.contrib import admin

from .models import (
    Section,
    Image,
    Index, Page, PageSectionMeta
)

admin.site.register(Image)
admin.site.register(Section)

admin.site.register(Index)
admin.site.register(Page)
admin.site.register(PageSectionMeta)
