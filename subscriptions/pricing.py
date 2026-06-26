"""Calcul du prix d'une souscription LOA"""

from decimal import Decimal

from catalog.models import Vehicle


def calculer_devis(vehicule, options, duree_mois=36):
    """Calcule le récapitulatif tarifaire d'une location longue durée.

    - loyer_base : estimation du loyer mensuel du véhicule (méthode Vehicle).
    - total_mensuel : loyer_base + somme des options mensuelles.
    - total_engagement : total_mensuel x durée.

    Lève ValueError si le véhicule n'est pas en location ou si la durée est invalide
    """
    if duree_mois <= 0:
        raise ValueError("La durée doit être strictement positive.")
    if vehicule.mode != Vehicle.Mode.LOCATION:
        raise ValueError("Ce véhicule n'est pas proposé à la location.")

    loyer_base = vehicule.estimation_loyer_mensuel(duree_mois)
    options_mensuel = sum((o.prix_mensuel for o in options), Decimal("0.00"))
    total_mensuel = (loyer_base + options_mensuel).quantize(Decimal("0.01"))
    total_engagement = (total_mensuel * duree_mois).quantize(Decimal("0.01"))

    return {
        "loyer_base": loyer_base,
        "options": [
            {"code": o.code, "libelle": o.libelle, "prix_mensuel": o.prix_mensuel}
            for o in options
        ],
        "duree_mois": duree_mois,
        "total_mensuel": total_mensuel,
        "total_engagement": total_engagement,
    }
