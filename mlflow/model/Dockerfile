# Utiliser une image Python légère
FROM python:3.14-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le script et le dossier bdd (pour le CSV)
COPY modelTraining.py .
COPY ../bdd ./bdd

# Commande par défaut pour exécuter le script
CMD ["python", "modelTraining.py"]