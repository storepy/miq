from django.urls import path, include

urlpatterns = [path('', include('miq.urls', namespace='miq')), ]

# from django.contrib import admin
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]

# urlpatterns += [
#     # path('', include('apps.documents.urls', namespace='documents')),
#     path('', include('grio.urls', namespace='grio')),
# ]

# # Must be last
# urlpatterns += [

# ]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
