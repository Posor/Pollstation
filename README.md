# PollStation - API REST de Sondages Anonymes

PollStation est une API REST développée dans le cadre du module "Applications distribuées". Elle permet de créer des sondages, de collecter des votes anonymes (via UUID) et de consulter des résultats agrégés.

> L'API est accessible sur `http://localhost:8000`.

> La documentation interactive (Swagger UI) est disponible sur `http://localhost:8000/docs`.

## Installation et Lancement

### Prérequis
- Python 3.10
- Pip

### Installation
```bash
# Création de l'environnement virtuel
python -m venv .venv

# Activation de l'environnement (sur linux)
source .venv/bin/activate

# Installation des dépendances (FastAPI, ORM et Outils de test)
pip install fastapi uvicorn sqlalchemy pydantic pytest httpx
```

### Lancement du serveur
```bash
uvicorn main:app --reload
```

### Execution des tests
```bash
pytest
```

---

## Choix d'Architecture (Basés sur les TD)

L'application a été découpée selon l'**Architecture en couches** vue en cours pour garantir la maintenabilité, la lisibilité et la séparation des responsabilités.

1. **Couche Controller (`controllers/`) - *TD 3***
   - Gère exclusivement les requêtes HTTP (FastAPI). 
   - Utilisation des codes HTTP sémantiques (200, 201 pour la création, 204 pour la suppression sans body).
   - Utilisation de l'injection de dépendances `Depends(get_db)` pour passer la session proprement.

2. **Couche Service (`services/`) - *TD 1 & TD 3***
   - Contient la totalité de la logique métier.
   - C'est cette couche qui protège l'application, elle effectue les vérifications et lève des `HTTPException` avant même de solliciter la base de données.

3. **Couche DAO (`dao/`) - *TD 2***
   - Gère les accès à la base de données via SQLAlchemy. Ne contient aucune logique métier, garantissant la changeabilité de la base si besoin.

4. **Modèles & Schémas (`models/` & `schemas/`) - *TD 2 & TD 3***
   - **SQLAlchemy** pour la BDD (SQLite). Utilisation des relations avec l'option `cascade="all, delete-orphan"` pour garder une base propre.
   - **Pydantic** pour la validation des entrées/sorties, avec `from_attributes = True` pour la sérialisation des objets ORM.

---

## Gestion des Erreurs et Robustesse

Conformément aux attentes du projet, une attention particulière a été portée pour **ne jamais faire crasher l'application** sur une entrée invalide. 
La stratégie suivante a été appliquée dans la couche Service :
- **400 Bad Request** : Levée lors du non-respect d'une règle de format.
- **404 Not Found** : Levée si la ressource demandée n'existe pas.
- **409 Conflict** : Levée pour protéger l'intégrité des données (ex: tentative de double vote avec le même `voter_token`, tentative de suppression d'un sondage possédant déjà des votes).
- **422 Unprocessable Entity** : Échec de validation Pydantic (ex: question trop courte).

Toutes ces erreurs renvoient un format JSON `{"detail": "message"}` pour faciliter l'intégration côté client et le passage des scripts de tests automatisés.

---

## Sécurité et Intégration

- **CORS (*TD 4*)** : Le `CORSMiddleware` a été intégré dans `main.py`.

---

## Fonctionnalités Bonus Implémentées

### Pagination (Route GET /polls)
Implémentation des paramètres `skip` (décalage) et `limit` (nombre de résultats) au niveau de la base de données pour optimiser la lecture des ressources.
- Exemple : `/polls?skip=0&limit=5`

### Tri (Route GET /polls)
Ajout d'un paramètre `sort` permettant d'ordonner les sondages par leur identifiant technique (date de création).
- `sort=desc` : Les plus récents en premier (comportement par défaut).
- `sort=asc` : Les plus anciens en premier.

### Tests automatisés
Mise en place de tests unitaires avec **Pytest** et **TestClient**.
Les tests vérifient :
- La validité des codes de retour HTTP (200, 400, 422).
- Le respect des règles métier (minimum 2 options par sondage).
- La robustesse de la validation Pydantic (longueur de question).
- Le fonctionnement mathématique de la limite de pagination.
