# TechMatch — Module 4 : Tests techniques & Feuille de route IA

> **ESPRIT — Cours : IA for Software Engineering | A.U 2026-2027**
> **Auteur : Aziz | Branche : `module4-aziz`**

---

## 📌 Description du module

Ce module fait partie de la plateforme **TechMatch** (recrutement de profils IT assisté par IA).

Il prend en charge :
- **Partie A** — Génération de tests techniques personnalisés par LLM + correction automatique
- **Partie B** — Génération de tests unitaires assistée par IA pour le code de l'équipe
- **Partie C** — Génération d'une feuille de route d'apprentissage personnalisée (bonus)

---

## 🏗️ Architecture

```
techmatch-module4/
├── app/
│   ├── main.py                          # Point d'entrée FastAPI
│   ├── config.py                        # Lecture du .env
│   ├── coreAgents/
│   │   ├── llm_client.py                # Client LLM (Groq) avec gestion erreurs
│   │   └── Agents/tech_assessment/
│   │       ├── generator.py             # Génération du test par LLM
│   │       ├── evaluator.py             # Correction des réponses par LLM
│   │       ├── roadmap.py               # Feuille de route par LLM
│   │       ├── prompts.py               # 3 versions de prompts (v1/v2/v3)
│   │       └── constants.py             # Constantes et schémas JSON
│   ├── db/
│   │   ├── base.py                      # Base SQLAlchemy
│   │   ├── session.py                   # Session BDD
│   │   └── models/tech_assessment.py    # 4 tables ORM
│   └── v1/
│       ├── schemas/tech_assessment.py   # Schémas Pydantic v2
│       └── endpoints/tech_assessment.py # 3 routes FastAPI
├── tests/
│   └── test_tech_assessment/
│       ├── test_schemas.py              # 24 tests Pydantic
│       ├── test_generator.py            # 8 tests générateur
│       └── test_evaluator_and_endpoints.py  # 7 tests évaluateur + API
├── scripts/
│   ├── ai_test_generator.py             # Génération de tests unitaires par IA
│   └── comparaison_modeles.py           # Comparaison gpt-oss-20b vs gpt-oss-120b
├── docs/
│   ├── prompts-aziz.md                  # Journal de prompts (3 versions)
│   └── comparaison_modeles.json         # Rapport de comparaison des modèles
└── requirements.txt
```

---

## 🚀 Installation et démarrage

### 1. Cloner le projet

```bash
git clone https://github.com/Gizenimohamedaziz/TechMatch.git
cd TechMatch
git checkout module4-aziz
```

### 2. Créer l'environnement virtuel

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer la clé API

Créer un fichier `.env` à la racine :

```env
LLM_API_KEY=ta_cle_groq_ici
LLM_BASE_URL=https://api.groq.com/openai
LLM_MODEL=openai/gpt-oss-120b
LLM_TIMEOUT_SECONDS=60
DATABASE_URL=
```

> 🔑 Obtenir une clé gratuite sur [console.groq.com](https://console.groq.com) → API Keys
> ⚠️ Ne jamais commiter le fichier `.env` sur GitHub

### 5. Lancer le serveur

```bash
python -m uvicorn app.main:app --reload --port 8080
```

Ouvrir la documentation interactive : **http://127.0.0.1:8080/docs**

---

## 🛣️ Routes API

| Méthode | Route | Description | Code retour |
|---------|-------|-------------|-------------|
| `POST` | `/api/v1/tests/generate` | Génère un test technique (5 questions + 1 exercice) | `201` |
| `POST` | `/api/v1/tests/{test_id}/submit` | Soumet les réponses et obtient la correction | `200` |
| `POST` | `/api/v1/roadmap` | Génère une feuille de route personnalisée | `201` |
| `GET`  | `/` | Santé du service | `200` |

### Exemple — Générer un test

```bash
curl -X POST http://127.0.0.1:8080/api/v1/tests/generate \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Développeur Backend Python",
    "job_description": "Nous recherchons un développeur Python junior.",
    "competences_manquantes": [
      {"skill": "Docker", "level": "débutant"},
      {"skill": "FastAPI", "level": "intermédiaire"}
    ],
    "candidate_id": "cand-anonyme-001"
  }'
```

### Paramètre optionnel — Version du prompt

```
POST /api/v1/tests/generate?prompt_version=v1   # Prompt minimal
POST /api/v1/tests/generate?prompt_version=v2   # Prompt structuré (défaut)
POST /api/v1/tests/generate?prompt_version=v3   # Chain-of-thought
```

---

## 🧪 Tests

### Tests unitaires (sans clé API — mocks)

```bash
python -m pytest tests/ -v
```

Résultat attendu : **39 passed**

### Tests d'intégration (avec vrai LLM)

```bash
# Démarrer le serveur d'abord
python -m uvicorn app.main:app --port 8080

# Dans un autre terminal
python _test_generate.py       # Test génération
python _test_flux_complet.py   # Test génération + correction
python _test_roadmap.py        # Test feuille de route
```

### Comparaison de modèles

```bash
python scripts/comparaison_modeles.py
```

Résultats obtenus :

| Modèle | Latence | Tokens | Conformité |
|--------|---------|--------|-----------|
| `gpt-oss-20b` | **1 177 ms** | 838 | 100% |
| `gpt-oss-120b` | 2 138 ms | 997 | 100% |

---

## 🔒 Règles de sécurité respectées

| Règle (prof) | Implémentation |
|---|---|
| Jamais de données personnelles au LLM | Détection email dans la description → rejet `422` |
| Toute sortie IA validée avant affichage | Validation Pydantic v2 sur chaque réponse LLM |
| Gestion des erreurs API | Timeout, quota (429), clé absente (401), JSON invalide → `503` propre |
| Jamais de clé API dans le code | `.env` uniquement, ignoré par `.gitignore` |
| Code candidat jamais exécuté | Correction par LLM uniquement (pas de `exec()`) |

---

## 🤖 Modèles IA utilisés

| Modèle | Usage | Justification |
|--------|-------|---------------|
| `openai/gpt-oss-120b` | Production (génération, correction, roadmap) | Meilleure qualité |
| `openai/gpt-oss-20b` | Comparaison / dev rapide | 2x plus rapide, moins de tokens |

Provider : **Groq** (API OpenAI-compatible, gratuit en développement)

---

## 📝 Journal de prompts

Voir [`docs/prompts-aziz.md`](docs/prompts-aziz.md) pour :
- Les 3 versions de prompts (v1 minimal, v2 structuré, v3 chain-of-thought)
- La justification du choix de modèle
- Les métriques mesurées (latence, tokens, conformité)

---

## 👥 Équipe TechMatch

| Module | Description | Membre |
|--------|-------------|--------|
| Module 1 | Parsing CV, anonymisation, RAG compétences | — |
| Module 2 | Matching CV/offre, audit équité | — |
| Module 3 | Analyse GitHub, revue de code IA | — |
| **Module 4** | **Tests techniques, évaluation IA, feuille de route** | **Aziz** |
| Module 5 | Plateforme, auth, BDD, CI/CD | — |

---

## 📦 Stack technique

- **Backend** : FastAPI + Uvicorn
- **Validation** : Pydantic v2
- **Base de données** : SQLite (dev) / PostgreSQL (prod)
- **ORM** : SQLAlchemy 2.x
- **LLM** : Groq API (`openai/gpt-oss-120b`)
- **Tests** : pytest 9.x
- **Python** : 3.12+
