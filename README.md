# M-Motors — API (back-end)

API REST de la refonte M-Motors: vente de véhicules d'occasion et location longue durée avec option d'achat (LOA). Front React dans le dépôt `m-motors-frontend`.

## Stack

Python 3.9.13 · Django 5.2 + Django REST Framework - JWT (simplejwt) - PostgreSQL (SQLite en local) - django-filter - Gunicorn + WhiteNoise - Sentry.

## Applications

| App | EPIC | Rôle |
| --- | --- | --- |
| `accounts` | E2 | Compte par e-mail, JWT, profil `/me/` |
| `catalog` | E1 / E6 | Véhicules, recherche filtrée, bascule vente/location (admin) |
| `dossiers` | E3 / E4 / E7 | Dossier + pièces, suivi de statut, validation/refus (admin) |
| `subscriptions` | E5 | Options, devis et souscription LOA (montants figés) |

## Lancer en local

```bash
python -m venv .venv && .venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env            # puis renseigner SECRET_KEY
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Sans `DATABASE_URL`, l'API tourne sur SQLite. Variables : voir `.env.example`.

## Tests

```bash
coverage run manage.py test && coverage report
```

## Git et branches

- Dépôt public. `main` stable, alimentée par Pull Request.
- Une branche par EPIC : `feature/E<n>-<sujet>`, commits `feat:`/`fix:`/`chore:`.
