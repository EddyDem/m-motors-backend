"""Administration des dossiers (back-office)"""

from django.contrib import admin

from dossiers.models import Document, Dossier


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0
    readonly_fields = ("cree_le",)


@admin.register(Dossier)
class DossierAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "type", "statut", "cree_le")
    list_filter = ("statut", "type")
    search_fields = ("client__email",)
    readonly_fields = ("cree_le", "maj_le")
    inlines = (DocumentInline,)
