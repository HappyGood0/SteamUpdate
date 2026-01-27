from llama_cloud import Pipeline
import mlflow
import mlflow.sklearn
import pandas as pd
from sklearn.base import accuracy_score
from sklearn.discriminant_analysis import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
# Configuration MLflow

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("topGamesUser")

print("📊 Chargement bdd topGamesUser")
data = pd.read_csv('../bdd/topGamesUser',sep=';')

data_train = data.head(int(len(data) * 0.8))
X_train = data_train.iloc[:, 3:]
y_train = data_train["score"]

data_test = data.tail(int(len(data) * 0.2))
X_test = data_test.iloc[:, 3:]
y_test = data_test["score"]

print("\n🚀 Entraînement du modèle avec MLflow...")

with mlflow.start_run(run_name="random_forest_topGamesUser"):
    
    # 1. Logger les paramètres
    params = {
        "n_estimators": 100,
        "max_depth": 5,
        "min_samples_split": 2,
        "random_state": 42
    }
    mlflow.log_params(params)
    
    # 2. Entraîner le modèle
    model = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler()),
    ("reg", RandomForestRegressor(**params)),
    ])

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    
    # 3. Logger les métriques
    metrics = {
        "accuracy": accuracy_score(y_test, predictions),
        "f1_score_macro": f1_score(y_test, predictions, average='macro'),
        "precision_macro": precision_score(y_test, predictions, average='macro'),
        "recall_macro": recall_score(y_test, predictions, average='macro'),
        "train_size": len(X_train),
        "test_size": len(X_test)
    }
    mlflow.log_metrics(metrics)
    
    print(f"✅ Accuracy: {metrics['accuracy']:.4f}")
    print(f"✅ F1-Score: {metrics['f1_score_macro']:.4f}")
    
    # 4. Logger le modèle
    mlflow.sklearn.log_model(
        model, 
        "model",
        registered_model_name="topGamesUser_regressor"
    )
    
    # 5. Logger un artefact (graphique)
    fig, ax = plt.subplots(figsize=(10, 6))
    feature_importance = model.named_steps['reg'].feature_importances_
    features = X_train.columns.tolist() 
    ax.barh(features, feature_importance)
    ax.set_xlabel('Importance')
    ax.set_title('Feature Importance')
    plt.tight_layout()
    
    # Sauvegarder et logger le graphique
    plt.savefig("feature_importance.png")
    mlflow.log_artifact("feature_importance.png")
    plt.close()
    
    # 6. Logger des tags pour organiser les runs
    mlflow.set_tags({
        "model_type": "RandomForest",
        "dataset": "topGamesUser",
        "team": "data-science",
        "environment": "training"
    })
    
    print(f"\n🎉 Run terminé! Consultez MLflow UI pour voir les résultats.")
    print(f"Run ID: {mlflow.active_run().info.run_id}")
