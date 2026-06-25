"""Administration de la souscription (back-office)"""

from django.contrib import admin

from subscriptions.models import Contract, Option


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ("libelle", "code", "prix_mensuel", "actif")
    list_filter = ("actif",)


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "vehicule", "total_mensuel", "statut", "cree_le")
    list_filter = ("statut",)
    search_fields = ("client__email",)
    readonly_fields = (
        "loyer_base",
        "total_mensuel",
        "total_engagement",
        "cree_le",
    )