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

print("\n🎉 Model Registry configuré! Consultez l'onglet 'Models' dans MLflow UI.")
