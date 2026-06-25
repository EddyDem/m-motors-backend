"""Administration du catalogue (back-office)"""

from django.contrib import admin

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
