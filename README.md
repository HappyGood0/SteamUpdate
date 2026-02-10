# Projet SteamUpdate

SteamUpdate (nom provisoire) présente une interface Web permettant de recommander un ou plusieurs jeux provenant du store Steam à un utilisateur, en fonction des jeux qu'il possède et auxquels il a joué.

## Graphes des services

![UML](UML.png)

## Utilisation

### Génération de la clé API Steam

1. Générer une clé API Steam sur https://steamcommunity.com/dev/apikey
2. Ajouter un fichier `.env` à la racine et ajouter `STEAM_API_KEY="VOTRE CLE"`

## Endpoints et interfaces

- **Frontend (web)** : [http://localhost:5173/](http://localhost:5173/)
- **Backend (API)** : [http://localhost:8000/](http://localhost:8000/)
- **API docs (Swagger)** : [http://localhost:8000/docs](http://localhost:8000/docs)
- **Metrics API** : [http://localhost:8000/metrics](http://localhost:8000/metrics)
- **Prometheus** : [http://localhost:9090/](http://localhost:9090/)
- **Grafana** : [http://localhost:3000/](http://localhost:3000/)
- **MLflow** : [http://localhost:5000/](http://localhost:5000/)

### Endpoints principaux

- `POST /api/recommend`  
  Recommande des jeux Steam à partir d'un identifiant Steam ou d'un pseudo Steam.
  - Payload : `{ "steam_id": "<id>" }` ou `{ "pseudo": "<pseudo>" }`
  - Réponse : liste de jeux recommandés

- `GET /api/health`  
  Vérifie que l'API est opérationnelle.

- `GET /api/metrics`  
  Expose les métriques Prometheus pour le monitoring.

## Pipeline CI/CD

- Les tests et le linting sont exécutés automatiquement à chaque push ou pull request grâce à GitHub Actions.
- Les workflows sont définis dans `.github/workflows/lint.yml` et `.github/workflows/tests.yml`.

## Vérification du linting

Pour vérifier et corriger le linting :

```bash
pip install ruff
ruff check .
ruff format --check .
ruff check . --fix
ruff format .
npm install -g eslint
eslint web/ --ext .js
```

## Convention de nommage des commits

- `feat: <message>`      # nouvelle fonctionnalité
- `fix: <message>`       # correction d'un bug
- `docs: <message>`      # mise à jour de la documentation
- `style: <message>`     # modification de css, d'indentation, etc.
- `refactor: <message>`  # rendre le code plus propre, plus adapté aux conventions, etc.
- `test: <message>`      # ajouter ou modifier des tests (unitaires et intégrations)
- `chore: <message>`     # gestion de dépendances ou des outils (.gitignore, fichiers de ce type)
- `ci: <message>`        # modification des fichiers de CI/CD

---

## Mise en place de Garage

1. Démarrer le service Garage avec Docker Compose :
```shell
docker compose up  -d
```

2. Vérifier que le service fonctionne :
```shell
docker exec -it garage /garage status
```
Mémoriser l'ID du node retourné.

3. Assigner un layout :
```shell
docker exec -it garage /garage layout assign -z dc1 -c 1G <node_id>
docker exec -it garage /garage layout apply --version 1
```

4. Créer un bucket de stockage puis vérifier sa création :
```shell
docker exec -it garage /garage bucket create mlflow-bucket
docker exec -it garage /garage bucket info mlflow-bucket
```

5. Créer une key pour le bucket puis l'assigner au bucket en lui donnant les permissions nécessaires :
```shell
docker exec -it garage /garage key create mlflow-key
docker exec -it garage /garage bucket allow --read --write --owner mlflow-bucket --key mlflow-key
```
Mémoriser la valeur de la key retournée (Key ID et Secret key).

6. Dans le fichier `docker-compose.yaml`, modifier les variables d'environnement `AWS_ACCESS_KEY_ID` et `AWS_SECRET_ACCESS_KEY` pour le service `mlflow` avec les valeurs de la key mémorisées précédemment.

## Démarrer le service MLFlow avec Docker Compose :

Après avoir réalisé les étapes de mise en place de Garage, démarrer le service MLFlow :
```shell
docker compose up -d
```

## Utiliser MLFlow :

L'interface MLFlow est accessible à l'adresse : [http://localhost:5000](http://localhost:5000).

Pour utiliser MLFlow avec Python, installer la bibliothèque :
```shell
pip install mlflow
```

## Créer le model : 

```shell
python3 ./mlflow/model/modelTraining.py
```