import os
import zipfile

def unzip_file(directory):
    # Parcourt tous les fichiers dans le répertoire
    for filename in os.listdir(directory):
        if filename.endswith('.zip'):
            zip_path = os.path.join(directory, filename)
            extract_dir = os.path.join(directory, os.path.splitext(filename)[0])

            # Crée le répertoire pour extraire les fichiers
            os.makedirs(extract_dir, exist_ok=True)
            
            # Décompresse le fichier zip
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
                print(f'Extracted {filename} to {extract_dir}')
            
            # Supprime le fichier zip après l'extraction
            os.remove(zip_path)
            print(f'Deleted {filename}')