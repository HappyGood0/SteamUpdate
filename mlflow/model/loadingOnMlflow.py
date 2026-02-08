import mlflow.sklearn
from mlflow.tracking import MlflowClient
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
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

model_name = "topGamesUser_regressor"

print("\n🚀 Entraînement du modèle...")

with mlflow.start_run(run_name="random_forest_latest"):
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    
    mlflow.log_param("model_type", "RandomForest")
    mlflow.log_param("n_estimators", 50)
    mlflow.log_metric("accuracy", accuracy)
    
    # Enregistrer le modèle dans le Registry
    model_info = mlflow.sklearn.log_model(
        model, 
        "model", 
        registered_model_name=model_name
    )
    
    print(f"✅ Modèle enregistré - Accuracy: {accuracy:.4f}")
    
    # ✅ Récupérer automatiquement la dernière version créée
    latest_version = model_info.registered_model_version
    
    print(f"\n📦 Nouvelle version créée: {latest_version}")

# ✅ Promouvoir LA DERNIÈRE VERSION en Staging
print(f"\n📌 Promotion de la version {latest_version} vers 'Staging'...")

try:
    # D'abord, rétrograder l'ancienne version Staging (s'il y en a une)
    staging_versions = client.get_latest_versions(model_name, stages=["Staging"])
    for old_version in staging_versions:
        print(f"   📥 Rétrogradation de la version {old_version.version} de Staging vers None")
        client.transition_model_version_stage(
            name=model_name,
            version=old_version.version,
            stage="None"
        )
    
    # Promouvoir la nouvelle version
    client.transition_model_version_stage(
        name=model_name, 
        version=latest_version,  # ✅ Utilise la version dynamiquement
        stage="Staging"
    )
    print(f"✅ Version {latest_version} déplacée vers Staging")
    
except Exception as e:
    print(f"⚠️ Impossible de changer le stage: {e}")

print("\n🎉 Model Registry configuré! Consultez l'onglet 'Models' dans MLflow UI.")