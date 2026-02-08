from prometheus_client import Counter, Histogram

recommendations_total = Counter(
    "recommendations_total", "Nombre total de recommandations générées", ["status"]
)

recommendation_response_time = Histogram(
    "recommendation_response_time_seconds",
    "Temps pour générer les recommandations de jeux",
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0, 60.0],
)

external_api_duration = Histogram(
    "external_api_duration_seconds",
    "Durée des appels aux APIs externes",
    ["api"],  # steam ou steamspy
    buckets=[0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)

external_api_errors_total = Counter(
    "external_api_errors_total",
    "Nombre total d'erreurs des APIs externes",
    ["api", "error_type"],  # error_type peut être 404, 500, timeout etc.
)

games_processed_per_recommendation = Histogram(
    "games_processed_per_recommendation",
    "Nombre de jeux analysés par requête de recommandation",
    buckets=[10, 50, 100, 200, 500, 1000, 2000, 5000],
)
