"""
WSGI config for finalWebsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application
from appartement.zipfile import unzip_file
from appartement.split_file import join_files

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finalWebsite.settings')

application = get_wsgi_application()

directory = os.path.join(os.getcwd(),'finalWebsite/appartement/RandomForestRegressor/models')
print(f'Files in the directory: {os.getcwd()}')
unzip_file(directory)

#parts_dir = './finalWebsite/appartement/RandomForestRegressor/models'  # Changez ce chemin si nécessaire

# Remplacez par le bon préfixe et chemin de sortie
parts_prefix = 'Auvergne-Rhone-Alpes.joblib.part'
output_file_path = os.path.join(os.getcwd(),'finalWebsite/appartement/RandomForestRegressor/models/Auvergne-Rhone-Alpes.joblib')
join_files(parts_prefix, output_file_path, directory)
# # Vérifie la taille finale du fichier recomposé
# print(f"Taille finale du fichier recomposé: {os.path.getsize(output_file_path)} octets")
#
parts_prefix = 'Nouvelle-Aquitaine.joblib.part'
output_file_path = os.path.join(os.getcwd(),'finalWebsite/appartement/RandomForestRegressor/models/Nouvelle-Aquitaine.joblib')
join_files(parts_prefix, output_file_path, directory)
# # Vérifie la taille finale du fichier recomposé
# print(f"Taille finale du fichier recomposé: {os.path.getsize(output_file_path)} octets")

parts_prefix = 'Occitanie.joblib.part'
output_file_path = os.path.join(os.getcwd(),'finalWebsite/appartement/RandomForestRegressor/models/Occitanie.joblib')
join_files(parts_prefix, output_file_path, directory)
# # Vérifie la taille finale du fichier recomposé
# print(f"Taille finale du fichier recomposé: {os.path.getsize(output_file_path)} octets")