import os
import zipfile

def unzip_file(directory):
    for filename in os.listdir(directory):
        if filename.endswith('.zip'):
            zip_path = os.path.join(directory, filename)
            
            # Décompresse le fichier zip
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                for file in zip_ref.namelist():
                    zip_ref.extract(file, directory)
                    print(f'Extracted {file} from {filename} to {directory}')
            
            # Supprime le fichier zip après l'extraction
            os.remove(zip_path)
            print(f'Deleted {filename}')