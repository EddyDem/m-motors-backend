"""Administration du catalogue (back-office)"""

from django.contrib import admin, messages
from django.utils.translation import ngettext

from catalog.models import Vehicle


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = (
        "marque",
        "modele",
        "motorisation",
        "kilometrage",
        "prix",
        "mode",
        "disponible",
        "cree_le",
    )
    list_filter = ("motorisation", "mode", "disponible")
    search_fields = ("marque", "modele")
    actions = ("passer_en_location", "passer_en_vente")

    @admin.action(description="Passer en location")
    def passer_en_location(self, request, queryset):
        nb = queryset.update(mode=Vehicle.Mode.LOCATION)
        self.message_user(
            request,
            ngettext(
                "%d véhicule passé en location.",
                "%d véhicules passés en location.",
                nb,
            ) % nb,
            messages.SUCCESS,
        )
        
    @admin.action(description="Passer en vente")
    def passer_en_vente(self, request, queryset):
        nb = queryset.update(mode=Vehicle.Mode.ACHAT)
        self.message_user(
            request,
            ngettext(
                "%d véhicule passé en vente.",
                "%d véhicules passés en vente.",
                nb,
            ) % nb,
            messages.SUCCESS,
        )