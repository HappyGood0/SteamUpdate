from pathlib import Path

import matplotlib.pyplot as plt
import mlflow.sklearn
import pandas as pd
from mlflow.models.signature import infer_signature
from mlflow.tracking import MlflowClient
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

import mlflow

# Configuration MLflow

mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("topGamesUser")

print("📊 Chargement bdd topGamesUser")

csv_path = Path(__file__).resolve().parents[2] / "bdd" / "topGamesUser.csv"
data = pd.read_csv(csv_path, sep=",")

csv_path2 = Path(__file__).resolve().parents[2] / "bdd" / "usersProfil.csv"
data2 = pd.read_csv(csv_path2, sep=",")

data["ID"] = data["ID"].astype(int)
data2["ID"] = data2["ID"].astype(int)

# split 80% train / 20% test ; retirer la première ligne demandée uniquement du train
n_train_data = int(len(data) * 0.8)
n_train_data2 = int(len(data2) * 0.8)

data_train = data.head(n_train_data).iloc[1:].reset_index(drop=True)
data_test = data.iloc[n_train_data:].reset_index(drop=True)

data2_train = data2.head(n_train_data2).iloc[1:].reset_index(drop=True)
data2_test = data2.iloc[n_train_data2:].reset_index(drop=True)

data3_train = pd.merge(data_train, data2_train, on="ID")
data3_test = pd.merge(data_test, data2_test, on="ID")
colonnes_tags = [c for c in data_train.columns if c not in ["ID", "score", "nom"]]
train_final = data3_train[["ID", "score", "nom_x"]].copy()
test_final = data3_test[["ID", "score", "nom_x"]].copy()
train_final = train_final.rename(columns={"nom_x": "nom"})
test_final = test_final.rename(columns={"nom_x": "nom"})
for tag in colonnes_tags:
    train_final[tag] = data3_train[f"{tag}_x"] - data3_train[f"{tag}_y"]
    test_final[tag] = data3_test[f"{tag}_x"] - data3_test[f"{tag}_y"]


X_train = train_final[colonnes_tags]
y_train = train_final["score"]

X_test = test_final[colonnes_tags]
y_test = test_final["score"]

X_train = X_train.abs()
X_test = X_test.abs()

print("\n🚀 Entraînement du modèle avec MLflow...")

with mlflow.start_run(run_name="random_forest_topGamesUser"):
    # 1. Logger les paramètres
    params = {"n_estimators": 100, "max_depth": 50, "min_samples_split": 2, "random_state": 42}
    mlflow.log_params(params)

    # 2. Entraîner le modèle
    model = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            ("reg", RandomForestRegressor(**params)),
        ]
    )

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    # 3. Logger les métriques
    metrics = {
        "mse": mean_squared_error(y_test, predictions),
        "mae": mean_absolute_error(y_test, predictions),
        "r2": r2_score(y_test, predictions),
        "train_size": len(X_train),
        "test_size": len(X_test),
    }
    mlflow.log_metrics(metrics)

    print(f"✅ MSE: {metrics['mse']:.4f}")
    print(f"✅ MAE: {metrics['mae']:.4f}")
    print(f"✅ R2: {metrics['r2']:.4f}")

    # 4. Logger le modèle
    # 4. Logger le modèle
    print("📦 Envoi du modèle au registre MLflow...")

    signature = infer_signature(X_train, model.predict(X_train))

    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        signature=signature,
        registered_model_name="topGamesUser_regressor",
    )
    print("✅ Modèle enregistré et répertorié !")
    # 5. Logger un artefact (graphique)
    fig, ax = plt.subplots(figsize=(10, 15))  # Augmente la hauteur car 81 tags c'est beaucoup !

    # On récupère l'importance des caractéristiques depuis le RandomForest à l'intérieur du pipeline
    feature_importance = model.named_steps["reg"].feature_importances_

    # On s'assure de prendre les noms des colonnes telles qu'elles ont été envoyées au modèle
    features = X_train.columns.tolist()

    # Tri pour avoir les plus importants en haut
    sorted_idx = feature_importance.argsort()

    ax.barh([features[i] for i in sorted_idx], feature_importance[sorted_idx])
    ax.set_xlabel("Importance")
    ax.set_title("Importance des Tags dans la recommandation")

    plt.tight_layout()
    plt.savefig("feature_importance.png")
    mlflow.log_artifact("feature_importance.png")
    plt.close(fig)
    # Sauvegarder et logger le graphique
    plt.savefig("feature_importance.png")
    mlflow.log_artifact("feature_importance.png")
    plt.close()

    # 6. Logger des tags pour organiser les runs
    mlflow.set_tags(
        {
            "model_type": "RandomForest",
            "dataset": "topGamesUser",
            "team": "data-science",
            "environment": "training",
        }
    )

    print("\n🎉 Run terminé! Consultez MLflow UI pour voir les résultats.")
    print(f"Run ID: {mlflow.active_run().info.run_id}")

    try:
        mlflow_client = MlflowClient()
        mlflow_client.transition_model_version_stage(
            name="topGamesUser_regressor", version=1, stage="Staging"
        )
        print("✅ Version 1 déplacée vers Staging")
    except Exception as e:
        print(f"⚠️  Impossible de changer le stage: {e}")

mlflow.end_run()
