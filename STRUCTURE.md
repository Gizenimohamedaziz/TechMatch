techmatch-module4/
├── app/
│   ├── main.py                          ← démarrage FastAPI
│   ├── config.py                        ← variables d'environnement (.env)
│   ├── coreAgents/
│   │   └── Agents/
│   │       └── tech_assessment/
│   │           ├── constants.py         ← constantes (profils LLM, callers)
│   │           ├── prompts.py           ← 3 versions de prompts (v1/v2/v3)
│   │           ├── generator.py         ← génération test via LLM
│   │           ├── evaluator.py         ← correction réponses via LLM
│   │           └── roadmap.py           ← feuille de route via LLM
│   ├── db/
│   │   ├── base.py                      ← base SQLAlchemy
│   │   ├── session.py                   ← session BDD
│   │   └── models/
│   │       └── tech_assessment.py       ← 4 tables BDD
│   └── v1/
│       ├── schemas/
│       │   └── tech_assessment.py       ← schémas Pydantic (validation I/O)
│       └── endpoints/
│           └── tech_assessment.py       ← 3 routes API
├── tests/
│   └── test_tech_assessment/
│       ├── test_schemas.py              ← 24 tests Pydantic
│       ├── test_generator.py            ← 8 tests générateur
│       └── test_evaluator_and_endpoints.py ← 7 tests endpoints
├── scripts/
│   └── ai_test_generator.py             ← Partie B : génération tests IA
├── docs/
│   └── prompts-aziz.md                  ← journal de prompts (notation)
├── .env.example                         ← modèle de configuration
├── .gitignore
└── requirements.txt
