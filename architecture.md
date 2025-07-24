```
m7b0/                           # Racine du projet
│ 
├── ai-api/                     # Répertoire de l'API de prédiction
│   ├── models/                 # Répertoire des modules d'entrainement du modèle
│   │   ├── prediction.py       # Méthodes utilitaires pour la prédiction
│   │   ├── preprocessor.py     # Méthodes utilitaires pour le preprocessing
│   │   └── training.py         # Script principal pour entraîner le modèle
│   ├── routes/                 # Répertoire des routes de l'API de prédiction
│   │   ├── health.py           # Routes de santé de l'API
│   │   └── model.py            # Routes relatives au modèle
│   ├── schemas/                # Répertoire des schemas Pydantic
│   │   └── prediction.py       # Schemas concernant la prédiction
│   ├── scripts/                # Répertoire des scripts
│   ├── config.py               # Fichier d'import des variables d'environnement du .env
│   ├── main.py                 # Entrypoint de l’API REST pour servir le modèle
│   ├── requirements.txt        # Dépendances spécifiques à l'API FastAPI
│   └── Dockerfile              # Image Docker pour conteneuriser l’API de prédiction
│
├── data/                       # Répertoire pour gérer les données du projet
│   ├── raw/                    # Données brutes non modifiées (CSV et parquet initiaux, etc.)
│   └── processed/              # Données nettoyées et transformées prêtes pour l'entraînement
│
├── data-api/                   # Microservice pour gérer la base de données et migrations
│   ├── alembic/                # Répertoire pour `env.py` et `versions/` Alembic
│   ├── crud/                   # Fonctions CRUD (Create, Read, Update, Delete)
│   │   ├── base.py             # Classe de CRUD de base
│   │   └── flight.py           # Exemple d'instanciation de la classe CRUD de base avec les resources relatives aux vols
│   ├── database/               # Répertoire pour les modules relatifs à la base de données
│   │   ├── engine.py           # Création de la session DB, moteur SQLAlchemy
│   │   └── seeder.py           # Script permettant de seeder la base de données à partir des csv stockés dans ./data/processed
│   ├── models/                 # Répertoire pour les modèles de données SQLAlchemy
│   │   └── flight.py           # Exemple de modèle de données sqlAlchemy pour les vols
│   ├── routes/                 # Répertoire pour les routes FastApi
│   │   ├── base_router.py      # Router de base sur lequel sont construits tous les autres
│   │   ├── health.py           # Routes de santé de l'API de données
│   │   └── flight.py           # Exemple de routes CRUD basées sur base_router.py pour les vols
│   ├── schemas/                # Répertoire pour les schémas Pydantic
│   │   └── flight.py           # Exemple de modèle de données sqlAlchemy pour les vols
│   ├── alembic.ini             # Fichier de configuration Alembic
│   ├── main.py                 # Entrypoint FastAPI pour exposer l’API interne de la BDD
│   ├── requirements.txt        # Dépendances spécifiques au service DB
│   └── Dockerfile              # Image Docker pour conteneuriser l’API BDD + migrations
│
├── monitoring/               # Configuration pour le monitoring avec Kuma, Prometheus & Grafana
│   ├── kuma/                 # Configs spécifiques à Kuma pour collecter des métriques
│   │   ├── kuma_config.yml   # Configuration principale pour Kuma
│   │   └── kuma_agent.yml    # Agent Kuma à déployer dans chaque service pour collecter les métriques
│   ├── prometheus/           # Config de Prometheus pour scraper les métriques
│   │   └── prometheus.yml    # Fichier de configuration de Prometheus pour scraper Kuma
│   ├── grafana/              # Configs Grafana : dashboards et datasources
│   │   ├── dashboards/       # Définition des dashboards Grafana
│   │   │   ├── dashboards.yml  # Fichier d'import pour dashboards
│   │   │   └── system-dashboard.yml # Exemple de dashboard système
│   │   ├── datasources/      # Config datasources Grafana (Prometheus, DB, etc.)
│   │   │   └── datasource.yml # Définition des connexions datasources
│   └── Dockerfile            # Image Docker pour conteneuriser les services de monitoring
│
├── mlruns/                   # Répertoire pour stocker les artefacts modèles versionnés via MLflow
│   ├── model_v1/             # Version 1 du modèle sauvegardée (fichiers MLflow)
│   └── model_v2/             # Version 2 du modèle (itération améliorée)
│
├── notebooks/                # Notebooks Jupyter pour exploration et prototypage
│
├── tests/                    # Tests unitaires et tests end-to-end
│   ├── test_training.py      # Tests pour vérifier le pipeline d'entraînement
│   ├── test_api.py           # Tests pour l'API de prédiction (routes, réponse)
│   ├── test_db.py            # Tests pour l'API BDD (CRUD, connexion)
│   └── test_monitoring.py    # Tests basiques du monitoring (endpoint Kuma)
│
├── docker-compose.yml        # Orchestration multi-conteneurs (API, DB, monitoring)
├── Makefile                  # Commandes utiles : lint, test, build, format, etc.
├── requirements.txt          # Dépendances globales pour tout le projet
├── .env                      # Variables d'environnement (ex. : URL DB, secrets)
├── .gitignore                # Fichiers/dossiers à ignorer dans le versioning Git
└── README.md                 # Documentation principale : usage, architecture, setup
```