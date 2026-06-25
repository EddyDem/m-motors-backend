"""Routage racine de l'API"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("accounts.urls")),
    path("api/", include("catalog.urls")),
    path("api/", include("dossiers.urls")),
]

if settings.DEBUG:
    # Sert les fichiers telecharges en dev (en prod: Supabase Storage)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
