import os

def split_file(file_path, chunk_size_mb):
    chunk_size = chunk_size_mb * 1024 * 1024  # Convertir MB en bytes
    with open(file_path, 'rb') as f:
        chunk = f.read(chunk_size)
        part_number = 1
        while chunk:
            part_file = f"{file_path}.part{part_number}"
            with open(part_file, 'wb') as part:
                part.write(chunk)
            part_number += 1
            chunk = f.read(chunk_size)

# file_path = './RandomForestRegressor/models/Nouvelle-Aquitaine.joblib'
# split_file(file_path, 40)  # Diviser en parties de 100 Mo
# file_path = './RandomForestRegressor/models/Occitanie.joblib'
# split_file(file_path, 40)  # Diviser en parties de 100 Mo
# /Users/thomas/Documents/Ecole/4A_ESGI/S2/PA_Render/finalWebsite/appartement/RandomForestRegressor/models/Provence-Alpes-Côte d'Azur.joblib



def join_files(parts_prefix, output_file_path, parts_dir='.'):
    # Liste les fichiers qui commencent par parts_prefix dans le répertoire spécifié
    parts = sorted([f for f in os.listdir(parts_dir) if f.startswith(parts_prefix)])

    # Affiche les fichiers trouvés pour vérification
    print("Fichiers trouvés pour recomposition:", parts)

    # Crée et écrit dans le fichier de sortie
    with open(output_file_path, 'wb') as output_file:
        for part in parts:
            part_path = os.path.join(parts_dir, part)
            with open(part_path, 'rb') as part_file:
                data = part_file.read()
                output_file.write(data)
                # Affiche la taille des données lues pour chaque fichier de partition
                print(f"Ajouté {len(data)} octets depuis {part_path}")


parts_dir = os.path.join(os.getcwd(),'finalWebsite/appartement/RandomForestRegressor/models')  # Changez ce chemin si nécessaire

# Remplacez par le bon préfixe et chemin de sortie
# parts_prefix = 'Auvergne-Rh\ône-Alpes.joblib.part'
# output_file_path = os.path.join(os.getcwd(),'finalWebsite/appartement/RandomForestRegressor/models/Auvergne-Rhône-Alpes.joblib')
# join_files(parts_prefix, output_file_path, parts_dir)
# # Vérifie la taille finale du fichier recomposé
# print(f"Taille finale du fichier recomposé: {os.path.getsize(output_file_path)} octets")
#
# parts_prefix = 'Nouvelle-Aquitaine.joblib.part'
# output_file_path = os.path.join(os.getcwd(),'finalWebsite/appartement/RandomForestRegressor/models/Nouvelle-Aquitaine.joblib')
# join_files(parts_prefix, output_file_path, parts_dir)
# # Vérifie la taille finale du fichier recomposé
# print(f"Taille finale du fichier recomposé: {os.path.getsize(output_file_path)} octets")

# parts_prefix = 'Occitanie.joblib.part'
# output_file_path = os.path.join(os.getcwd(),'finalWebsite/appartement/RandomForestRegressor/models/Occitanie.joblib')
# join_files(parts_prefix, output_file_path, parts_dir)
# # Vérifie la taille finale du fichier recomposé
# print(f"Taille finale du fichier recomposé: {os.path.getsize(output_file_path)} octets")