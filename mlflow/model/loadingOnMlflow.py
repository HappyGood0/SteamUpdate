"""
Script 2: Model Registry - Gestion des versions de modèles
===========================================================
Ce script démontre comment:
- Enregistrer un modèle dans le Model Registry
- Gérer les versions de modèles
- Changer les stages (None, Staging, Production, Archived)
- Ajouter des descriptions et tags aux versions
"""

import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.datasets import load_iris
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

import mlflow

# Configuration MLflow
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("02-Model-Registry")

# Initialiser le client MLflow
client = MlflowClient()

# Chargement des données
print("📊 Chargement bdd topGamesUser")
data = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.2, random_state=42
)

model_name = "iris_classifier_registry"

# ====================
# VERSION 1: Random Forest
# ====================
print("\n🚀 Entraînement VERSION 1 - RandomForest...")
with mlflow.start_run(run_name="v1_random_forest"):
    model_v1 = RandomForestClassifier(n_estimators=50, random_state=42)
    model_v1.fit(X_train, y_train)

    predictions = model_v1.predict(X_test)
    accuracy_v1 = accuracy_score(y_test, predictions)

    mlflow.log_param("model_type", "RandomForest")
    mlflow.log_param("n_estimators", 50)
    mlflow.log_metric("accuracy", accuracy_v1)

    # Enregistrer le modèle dans le Registry
    model_uri = mlflow.sklearn.log_model(
        model_v1, "model", registered_model_name=model_name
    ).model_uri

    print(f"✅ Version 1 - Accuracy: {accuracy_v1:.4f}")
    run_id_v1 = mlflow.active_run().info.run_id

# Promouvoir la version 1 en Staging
print("\n📌 Promotion de la version 1 vers 'Staging'...")
try:
    client.transition_model_version_stage(name=model_name, version=1, stage="Staging")
    print("✅ Version 1 déplacée vers Staging")
except Exception as e:
    print(f"⚠️  Impossible de changer le stage: {e}")

# ====================
# VERSION 2: Gradient Boosting (meilleur modèle)
# ====================
print("\n🚀 Entraînement VERSION 2 - GradientBoosting...")
with mlflow.start_run(run_name="v2_gradient_boosting"):
    model_v2 = GradientBoostingClassifier(n_estimators=100, random_state=42)
    model_v2.fit(X_train, y_train)

    predictions = model_v2.predict(X_test)
    accuracy_v2 = accuracy_score(y_test, predictions)

    mlflow.log_param("model_type", "GradientBoosting")
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("accuracy", accuracy_v2)

    # Enregistrer le modèle dans le Registry
    mlflow.sklearn.log_model(model_v2, "model", registered_model_name=model_name)

    print(f"✅ Version 2 - Accuracy: {accuracy_v2:.4f}")
    run_id_v2 = mlflow.active_run().info.run_id

# Comparer les versions et promouvoir la meilleure en Production
print("\n📊 Comparaison des versions...")
print(f"Version 1 (RandomForest): {accuracy_v1:.4f}")
print(f"Version 2 (GradientBoosting): {accuracy_v2:.4f}")

if accuracy_v2 > accuracy_v1:
    print("\n🏆 Version 2 est meilleure! Promotion vers Production...")
    try:
        # Mettre la version 2 en Production
        client.transition_model_version_stage(name=model_name, version=2, stage="Production")

        # Archiver la version 1
        client.transition_model_version_stage(name=model_name, version=1, stage="Archived")
        print("✅ Version 2 en Production, Version 1 archivée")
    except Exception as e:
        print(f"⚠️  Impossible de changer les stages: {e}")
else:
    print("\n🏆 Version 1 reste la meilleure!")
    try:
        client.transition_model_version_stage(name=model_name, version=1, stage="Production")
        print("✅ Version 1 promue en Production")
    except Exception as e:
        print(f"⚠️  Impossible de changer le stage: {e}")

# Ajouter une description au modèle
print("\n📝 Ajout de métadonnées...")
try:
    client.update_registered_model(
        name=model_name,
        description="Classifieur Iris - Modèle de démonstration pour le cours DevMLOps",
    )

    # Ajouter des tags aux versions
    client.set_model_version_tag(
        name=model_name, version="1", key="validation_status", value="tested"
    )

    client.set_model_version_tag(
        name=model_name, version="2", key="validation_status", value="tested"
    )
    print("✅ Métadonnées ajoutées")
except Exception as e:
    print(f"⚠️  Erreur lors de l'ajout des métadonnées: {e}")

# Afficher toutes les versions du modèle
print(f"\n📋 Versions enregistrées pour '{model_name}':")
try:
    versions = client.search_model_versions(f"name='{model_name}'")
    for version in versions:
        print(
            f"  - Version {version.version}: Stage={version.current_stage}, Run ID={version.run_id}"
        )
except Exception as e:
    print(f"⚠️  Impossible de récupérer les versions: {e}")

print("\n🎉 Model Registry configuré! Consultez l'onglet 'Models' dans MLflow UI.")
