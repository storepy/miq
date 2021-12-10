from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import SiteSetting
from .models import Image, Thumbnail
from .models import Section
from .models import Index, Page, PageSectionMeta

CustomUser = get_user_model()


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # add_form = SignupForm
    # form = CustomUserChangeForm
    list_display = [
        'username', 'first_name',
        'last_name', 'email', 'gender',
    ]
    search_fields = ['username', 'email', 'slug']


# admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Image)
admin.site.register(Thumbnail)

admin.site.register(SiteSetting)

admin.site.register(Section)

admin.site.register(Index)


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('label', 'slug_public', 'slug')


admin.site.register(PageSectionMeta)
