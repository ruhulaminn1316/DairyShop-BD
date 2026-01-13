from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ MUST: allauth
    path('accounts/', include('allauth.urls')),

    # your app urls
    path('', include('app.urls')),

    path('adminpanel/', include('adminpanel.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
