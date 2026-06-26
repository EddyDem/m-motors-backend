"""Administration des dossiers (back-office)"""

from django import forms
from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.utils.translation import ngettext

from dossiers.models import Document, Dossier


class DocumentInline(admin.TabularInline):
    model = Document
    extra = 0
    readonly_fields = ("cree_le",)


class MotifRefusForm(forms.Form):
    """Formulaire intermédiaire: saisie du motif lors d'un refus"""

    motif = forms.CharField(
        label="Motif du refus",
        widget=forms.Textarea(attrs={"rows": 3}),
        required=True,
    )


@admin.register(Dossier)
class DossierAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "type", "statut", "cree_le")
    list_filter = ("statut", "type")
    search_fields = ("client__email",)
    readonly_fields = ("cree_le", "maj_le")
    inlines = (DocumentInline,)
    actions = ("valider_dossiers", "refuser_dossiers")

    @admin.action(description="Valider les dossiers sélectionnés")
    def valider_dossiers(self, request, queryset):
        for dossier in queryset:
            dossier.valider()
        nb = queryset.count()
        self.message_user(
            request,
            ngettext("%d dossier validé.", "%d dossiers validés.", nb) % nb,
            messages.SUCCESS,
        )

    @admin.action(description="Refuser les dossiers sélectionnés (motif requis)")
    def refuser_dossiers(self, request, queryset):
        # Étape 2: le formulaire a été posté -> on applique le refus
        if "appliquer" in request.POST:
            form = MotifRefusForm(request.POST)
            if form.is_valid():
                motif = form.cleaned_data["motif"]
                for dossier in queryset:
                    try:
                        dossier.refuser(motif)
                    except ValidationError as exc:
                        self.message_user(request, exc.messages[0], messages.ERROR)
                        return None
                nb = queryset.count()
                self.message_user(
                    request,
                    ngettext("%d dossier refusé.", "%d dossiers refusés.", nb) % nb,
                    messages.SUCCESS,
                )
                return None
        else:
            form = MotifRefusForm()

        # Étape 1: afficher la page de saisie du motif
        return render(
            request,
            "refus_motif.html",
            {
                "dossiers": queryset,
                "form": form,
                "action": "refuser_dossiers",
                "title": "Motif de refus",
            },
        )
