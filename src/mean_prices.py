import csv
import json
from collections import defaultdict

csv_file = "../PA/Dataset/valeurs_foncieres_with_mean_price_neighborhood.csv"
output_file = "average_prices_by_departement.json"

departement_data = defaultdict(lambda: {'maison': {'total_value': 0, 'total_area': 0, 'count': 0},
                                        'appartement': {'total_value': 0, 'total_area': 0, 'count': 0}})

with open(csv_file, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=';')
    
    required_columns = ['dep_name', 'valeur_fonciere', 'surface_reelle_bati', 'type_local']
    for col in required_columns:
        if col not in reader.fieldnames:
            raise ValueError(f"Column '{col}' not found in the CSV file.")

    for row in reader:
        try:
            departement = row['dep_name']
            valeur_fonciere = float(row['valeur_fonciere'])
            superficie = float(row['surface_reelle_bati'])
            type_local = row['type_local'].lower()
            
            if type_local in ['maison', 'appartement']:
                departement_data[departement][type_local]['total_value'] += valeur_fonciere
                departement_data[departement][type_local]['total_area'] += superficie
                departement_data[departement][type_local]['count'] += 1
        except ValueError as e:
            print(f"Skipping row due to value error: {e}")
        except KeyError as e:
            print(f"Skipping row due to missing key: {e}")

average_prices = {}
for departement, types in departement_data.items():
    average_prices[departement] = {}
    for type_local, data in types.items():
        if data['count'] > 0 and data['total_area'] > 0:
            average_price = data['total_value'] / data['count']
            average_price_per_sqm = data['total_value'] / data['total_area']
            average_prices[departement][type_local] = {
                'average_price': average_price,
                'average_price_per_sqm': average_price_per_sqm
            }

with open(output_file, 'w', encoding='utf-8') as json_file:
    json.dump(average_prices, json_file, ensure_ascii=False, indent=4)

print(f"Average prices by departement have been written to {output_file}")
