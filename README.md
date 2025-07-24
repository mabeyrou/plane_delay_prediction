# Projet de Prédiction des Retards de Vols

## Description du Projet

Ce projet vise à prédire les retards de vols en utilisant des données historiques. L'objectif est de développer un modèle de machine learning capable de déterminer si un vol est susceptible d'être retardé, en se basant sur divers facteurs tels que la compagnie aérienne, l'aéroport de départ, l'heure de départ prévue, etc.
## 📊 Analyse des données

L'analyse des données a été compliquée par la quantité importante de données, rendant les traitements très compliqués avec mes ressources.  
J'ai donc travaillé avec des notebooks séparé pour épargné ma RAM. J'ai ensuite concaténé mes différents rendus en un seul notebook.
**Les rendus attendus :**
- notebooks/0-complete-notebook.ipynb
- notebooks/0-journal-de-bord.ipynb
**Les notebooks de travail :**
- notebooks/1-columns_analysis.ipynb.ipynb
- notebooks/2-to_parquet.ipynb
- notebooks/3-from_complete_parquet.ipynb
- notebooks/4-modelisation.ipynb

## 🏗️ Architecture

Vous trouverez une structure détaillée du projet ici : [architecture.md](architecture.md)

### Services Applicatifs
- **Backend (FastAPI)** : 
  - API pour les prédictions
  - API en lien avec la base de données (seule capable d'y accéder)
- **Frontend (Streamlit)** : Interface utilisateur web

### Stack de Monitoring
- **Prometheus** : Collecte des métriques
- **Grafana** : Visualisation des données
- **Node Exporter** : Métriques système
- **Uptime Kuma** : Monitoring de disponibilité

L'application est toujours en cours de développement. 

## 🚀 Installation
### Configuration
Le fichier `.env.example` contient toutes les variables d'environnement. 
Copiez le et remplissez le avec les valeurs appropriées :
```bash
cp .env.example .env
```
Quelques valeurs par défaut (non sensibles) ont été préservées.
### Lancement
```bash
# Démarrer tous les services
docker-compose up -d

# Vérifier le statut
docker-compose ps

# Voir les logs
docker-compose logs -f [service_name]
```

## 🌐 Accès aux Services

| Service | URL | Port | Description |
|---------|-----|------|-------------|
| **Frontend** | http://localhost:8501 | 8501 | Interface Streamlit |
| **Backend API** | http://localhost:8000 | 8000 | API FastAPI + Docs |
| **Grafana** | http://localhost:3000 | 3000 | Dashboards de monitoring |
| **Prometheus** | http://localhost:9090 | 9090 | Interface Prometheus |
| **Uptime Kuma** | http://localhost:3001 | 3001 | Monitoring uptime |

### Credentials par défaut
- **Grafana** : ceux fournis dans votre `.env` avec les variables d'environnement `GRAFANA_ADMIN_PASSWORD` et `GRAFANA_ADMIN_USER`
- **Autres services** : Pas d'authentification requise

## 📊 Dashboards Grafana

### Dashboard recommandé : Node Exporter Full (ID: 1860)
```bash
# Import automatique via provisioning ou manuel :
# 1. Aller dans Grafana > + > Import
# 2. Entrer l'ID : 1860
# 3. Sélectionner la datasource Prometheus
```

**Métriques disponibles :**
- CPU, RAM, Disque, Réseau
- Processus système
- Métriques de l'application

## 🔧 Configuration Monitoring

### Prometheus Targets
Les cibles sont configurées dans `prometheus/prometheus.yml` :
```yaml
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: "backend"
    static_configs:
      - targets: ["backend:8000"]

  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "node-exporter"
    static_configs:
      - targets: ["node-exporter:9100"]
```

### Grafana Datasource
La datasource Prometheus est automatiquement configurée via provisioning :
- **URL** : http://prometheus:9090
- **Accès** : Server (default)

## 🐳 Utilisation avec Images Docker Hub

Pour tester avec des images distantes :

### Modifier docker-compose.yml
```yaml
services:
  backend:
    image: marou974/m0b5-back:${APP_VERSION}
    # Commenter la section build:
    
  frontend:
    image: marou974/m0b5-front:${APP_VERSION}
    # Commenter la section build:
```

### Ajouter les variables dans .env
```bash
APP_VERSION=latest
```

### Relancer
```bash
docker-compose pull
docker-compose up -d
```

## 🔨 Commandes Utiles

### Gestion Docker
```bash
# Reconstruire les images
docker-compose build

# Redémarrer un service
docker-compose restart [service_name]

# Nettoyer les ressources
docker system prune -a

# Volumes spécifiques
docker volume prune
```

### Logs et Debug
```bash
# Logs en temps réel
docker-compose logs -f

# Logs d'un service spécifique
docker-compose logs backend

# Entrer dans un conteneur
docker exec -it [container_name] /bin/bash
```

## 🌐 Réseaux Docker

### Architecture réseau
- **app-network** : Communication backend ↔ frontend
- **monitoring** : Isolation du stack de monitoring

```yaml
networks:
  app-network:    # Application
  monitoring:     # Monitoring stack
```

## 🚨 Troubleshooting

### Problèmes courants

1. **Variables d'environnement non trouvées**
   ```bash
   # Vérifier la présence du fichier .env
   ls -la .env
   
   # Être dans le bon répertoire
   pwd
   ```

2. **Ports déjà utilisés**
   ```bash
   # Identifier les processus utilisant les ports
   sudo lsof -i :8000
   sudo lsof -i :3000
   ```

3. **Services qui ne démarrent pas**
   ```bash
   # Vérifier les logs d'erreur
   docker-compose logs [service_name]
   
   # Vérifier les dépendances
   docker-compose ps
   ```

## 📝 Développement

### Structure du projet
```
├── backend/           # API FastAPI
├── frontend/          # App Streamlit
├── prometheus/        # Config Prometheus
├── grafana/          # Provisioning Grafana
├── docker-compose.yml # Orchestration
└── .env              # Variables d'environnement
```

### Tests
```bash
# Tests backend
docker-compose exec backend python -m pytest

# Tests dans le conteneur
docker exec -it m5b0_backend_1 pytest
```

---

## 🤝 Support

Pour toute question ou problème :
1. Vérifier les logs : `docker-compose logs`
2. Consulter la documentation des services
3. Vérifier la configuration réseau Docker