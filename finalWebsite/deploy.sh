#!/bin/bash

# Installer Git LFS
echo "Installing Git LFS..."
apt-get update
apt-get install -y git-lfs

# Initialiser Git LFS
echo "Initializing Git LFS..."
git lfs install

# Cloner le dépôt avec Git LFS
echo "Cloning repository..."
git clone https://github.com/Useer923/PA-Render.git .

# Changer le répertoire de travail
# cd /path/to/your/app

# Mettre à jour les fichiers LFS
echo "Fetching LFS files..."
git lfs pull


# Installer les dépendances Python
echo "Installing dependencies..."
pip install -r requirements.txt


