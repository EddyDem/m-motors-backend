from django.db import migrations
from decimal import Decimal


def creer_options(apps, schema_editor):
    Option = apps.get_model("subscriptions", "Option")
    options = [
        ("assurance", "Assurance tous risques", Decimal("39.00")),
        ("assistance", "Assistance dépannage", Decimal("9.00")),
        ("sav", "Entretien et SAV", Decimal("25.00")),
        ("controle_technique", "Contrôle technique", Decimal("6.00")),
    ]
    for code, libelle, prix in options:
        Option.objects.update_or_create(
            code=code, defaults={"libelle": libelle, "prix_mensuel": prix}
        )


def supprimer_options(apps, schema_editor):
    Option = apps.get_model("subscriptions", "Option")
    Option.objects.filter(
        code__in=["assurance", "assistance", "sav", "controle_technique"]
    ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("subscriptions", "0001_initial"),
    ]
    operations = [
        migrations.RunPython(creer_options, supprimer_options),
    ]
