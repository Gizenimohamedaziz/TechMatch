"""
Module 4 TechMatch — Application FastAPI.
Auteur : Aziz (ESPRIT A.U 2026-2027)

Pour lancer : uvicorn app.main:app --reload
Swagger UI  : http://localhost:8000/docs
"""
from fastapi import FastAPI
from app.v1.endpoints.tech_assessment import router as tests_router, roadmap_router
from app.db.base import Base
from app.db.session import engine

# Créer les tables BDD automatiquement au démarrage (pratique en dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="TechMatch — Module 4 : Tests techniques",
    description=(
        "Génération de tests techniques par IA, correction des réponses "
        "et feuilles de route d'apprentissage personnalisées.\n\n"
        "**Auteur :** Aziz | **Cours :** IA for SE, ESPRIT A.U 2026-2027"
    ),
    version="1.0.0",
)

app.include_router(tests_router, prefix="/api/v1")
app.include_router(roadmap_router, prefix="/api/v1")


@app.get("/", tags=["Santé"])
def health():
    """Vérifie que le serveur fonctionne."""
    return {
        "status": "ok",
        "module": "Module 4 — Tests techniques",
        "auteur": "Aziz",
        "routes": [
            "POST /api/v1/tests/generate",
            "POST /api/v1/tests/{id}/submit",
            "POST /api/v1/roadmap",
        ],
    }
