# init_gaz_app.pyimport os

# Dossiers à créer
folders = [
    "r-gaz/backend/config",
    "r-gaz/backend/core",
    "r-gaz/backend/users",
    "r-gaz/backend/delivery",
    "r-gaz/backend/common",
    "r-gaz/backend/tests",
    "r-gaz/frontend",
    "r-gaz/docker/nginx",
    "r-gaz/scripts",
]

# Fichiers à créer
files = [
    "r-gaz/backend/manage.py",
    "r-gaz/docker/backend.dockerfile",
    "r-gaz/docker/docker-compose.yml",
    "r-gaz/.env",
    "r-gaz/.dockerignore",
    "r-gaz/.gitignore",
    "r-gaz/README.md",
    "r-gaz/init_gaz_app.py"
]

# Création des dossiers
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Création des fichiers
for file in files:
    with open(file, "w") as f:
        f.write(f"# {os.path.basename(file)}")

print("✅ Arborescence de r-gaz créée avec succès !")
