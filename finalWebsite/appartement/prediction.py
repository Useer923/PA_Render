from .models import load_transformer
import pandas as pd
from datetime import datetime
import joblib
import os

def predict_price_appartement(adresse_numero, adresse_suffixe, adresse_code_voie, adresse_nom_voie, region, code_postal, superficie, nombre_de_pieces, etage, ascenseur):

    today_date = datetime.now().strftime('%Y-%m-%d')

    df = pd.DataFrame({''
    'date-mutation': [today_date],
    'no-voie': [adresse_numero],
    'b/t/q': [adresse_suffixe],
    'type-de-voie': [adresse_code_voie],
    'voie': [adresse_nom_voie],
    'code-postal': [code_postal],
    'type-local': ['Appartement'],
    'surface-terrain': [0],
    'surface-reelle-bati': [superficie],
    'nombre-pieces-principales': [nombre_de_pieces]
})
    
    print("DataFrame:", df)
    print("Colonnes du DataFrame:", df.columns)

    transformer = load_transformer(os.path.join(os.getcwd(),f'finalWebsite/appartement/RandomForestRegressor/transformers/{region}.csv'))
    model = joblib.load(os.path.join(os.getcwd(),f'finalWebsite/appartement/RandomForestRegressor/models/{region}.joblib'))

    for column in df.columns:
        if df[column].isnull().any():
            print(f"Missing value found in column: {column}")
            df[column].fillna('', inplace=True)

    transformed_data = transformer.transform(df)
    base_predicted_price = model.predict(transformed_data)
    print(int(base_predicted_price))

    # Variable selon l'etage et presence d'ascenseur
    etage_adjustment_factors_idf = {
        'with_ascenseur': [0.887, 0.966, 1.0, 1.028, 1.039, 1.049, 1.054, 1.104],
        'without_ascenseur': [0.919, 0.983, 1.0, 1.022, 1.034, 1.003, 0.994, 1.044]
    }
    etage_adjustment_factors_province = {
        'with_ascenseur': [0.901, 0.991, 1.0, 1.014, 1.04],
        'without_ascenseur': [0.904, 0.981, 1.0, 0.991, 0.981, 0.919]
    }

    if region == 'Île-de-France':
        adjustment_factors = etage_adjustment_factors_idf['with_ascenseur'] if ascenseur else etage_adjustment_factors_idf['without_ascenseur']
    else:
        adjustment_factors = etage_adjustment_factors_province['with_ascenseur'] if ascenseur else etage_adjustment_factors_province['without_ascenseur']
    
    etage_index = min(etage, len(adjustment_factors) - 1)
    
    adjustment = adjustment_factors[etage_index]
    adjusted_price = base_predicted_price * adjustment
    print(adjustment)
    print(int(adjusted_price))

    return adjusted_price


def predict_price_maison(adresse_numero, adresse_suffixe, adresse_code_voie, adresse_nom_voie, region, code_postal, superficie, superficie_terrain, nombre_de_pieces):
    
    today_date = datetime.now().strftime('%Y-%m-%d')

    df = pd.DataFrame({''
    'date-mutation': [today_date],
    'no-voie': [adresse_numero],
    'b/t/q': [adresse_suffixe],
    'type-de-voie': [adresse_code_voie],
    'voie': [adresse_nom_voie],
    'code-postal': [code_postal],
    'type-local': ['Maison'],
    'surface-terrain': [superficie_terrain],
    'surface-reelle-bati': [superficie],
    'nombre-pieces-principales': [nombre_de_pieces]
})
    
    print("DataFrame:", df)
    print("Colonnes du DataFrame:", df.columns)

    transformer = load_transformer(os.path.join(os.getcwd(),f'finalWebsite/appartement/RandomForestRegressor/transformers/{region}.csv'))
    model = joblib.load(os.path.join(os.getcwd(),f'finalWebsite/appartement/RandomForestRegressor/models/{region}.joblib'))

    for column in df.columns:
        if df[column].isnull().any():
            print(f"Missing value found in column: {column}")
            df[column].fillna('', inplace=True)

    transformed_data = transformer.transform(df)
    predicted_price = model.predict(transformed_data)
    print(int(predicted_price))

    return predicted_price
