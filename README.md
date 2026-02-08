Readme
# Projet SteamUpdate

SteamUpdate (nom provisioire) présente une interface Web permettant de recommander un ou plusieurs jeux provenant du store Steam à un utilisateur, en fonction des jeux qu'il possède et auxquels il a joué.

## Graphes des services

![UML](UML.png)

## Utilisation

### Génération de la clé API Steam
[...]


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

Après avoir réaliser les étapes de mise en place de Garage, démarrer le service MLFlow :
```shell
docker compose up -d
```

## Utiliser MLFlow :

L'interface MLFlow est accessible à l'adresse : [http://localhost:5000](http://localhost:5000).

Pour utiliser MLFlow avec Python, installer la bibliothèque :
```shell
pip install mlflow
```
