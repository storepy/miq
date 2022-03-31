from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import SiteSetting
from .models import Image
from .models import Section
from .models import Index, Page

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

admin.site.register(Index)
admin.site.register(Section)

admin.site.register(SiteSetting)


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('label', 'meta_slug', 'slug')
