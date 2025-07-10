FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances système utiles
RUN apt-get update && apt-get install -y build-essential

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copier tout ton projet dans /app
COPY . .

# Exposer le port utilisé par FastAPI
EXPOSE 8000

# 👉 Lance l'app depuis son chemin correct
CMD ["uvicorn", "fastapi-opensearch.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
