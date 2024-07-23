from django.db import models
from django.utils import timezone
import pandas as pd


REGIONS_CHOICES = [
    ('', 'Sélectionnez votre région'),
    ('Auvergne-Rhône-Alpes', 'Auvergne-Rhône-Alpes'),
    ('Bourgogne-Franche-Comté', 'Bourgogne-Franche-Comté'),
    ('Bretagne', 'Bretagne'),
    ('Centre-Val de Loire', 'Centre-Val de Loire'),
    ('Corse', 'Corse'),
    ('Grand Est', 'Grand Est'),
    ('Hauts-de-France', 'Hauts-de-France'),
    ('Île-de-France', 'Île-de-France'),
    ('Normandie', 'Normandie'),
    ('Nouvelle-Aquitaine', 'Nouvelle-Aquitaine'),
    ('Occitanie', 'Occitanie'),
    ('Pays de la Loire', 'Pays de la Loire'),
    ('Provence-Alpes-Côte d\'Azur', 'Provence-Alpes-Côte d\'Azur')
]

TYPES_VOIE_CHOICES = [
    ('', '---'),
    ('ALL', 'Allée'),
    ('AV', 'Avenue'),
    ('BD', 'Boulevard'),
    ('CHE', 'Chemin'),
    ('RUE', 'Rue'),
    ('RTE', 'Route'),
    ('IMP', 'Impasse'),
    ('QUAI', 'Quai'),
    ('PL', 'Place'),
    ('PARC', 'Parc'),
    ('CRS', 'Cours'),
    ('RES', 'Résidence'),
    ('FG', 'Faubourg'),
    ('VOIE', 'Voie'),
    ('PTR', 'Porte'),
    ('PAS', 'Passage'),
    ('MAIL', 'Mail'),
    ('SEN', 'Sentier'),
    ('PTE', 'Petite Rue'),
    ('TRT', 'Traversée'),
    ('ZAC', 'Zone d\'Activité Commerciale'),
    ('ZI', 'Zone Industrielle')
]

SUFFIXE_CHOICES = [
    ('', '---'),
    ('T', 'Ter'),
    ('A', 'A'),
    ('B', 'Bis'),
    ('D', 'D'),
    ('G', 'G'),
    ('C', 'C'),
    ('F', 'F'),
    ('Q', 'Quater'),
]
    
class PredictionAppart(models.Model):
    adresse_numero = models.CharField(max_length=10, default='')
    adresse_suffixe = models.CharField(max_length=2, choices=SUFFIXE_CHOICES, blank=True, null=True, default='')
    adresse_code_voie = models.CharField(max_length=100, choices=TYPES_VOIE_CHOICES, default='')
    adresse_nom_voie = models.CharField(max_length=100, default='')
    code_postal = models.CharField(max_length=10)
    ville = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, choices=REGIONS_CHOICES, default='')
    departement = models.CharField(max_length=100)
    superficie = models.FloatField()
    nombre_de_pieces = models.IntegerField()
    etage = models.IntegerField()
    ascenseur = models.BooleanField(default=False)
    prix_estime = models.FloatField()
    date_predicted = models.DateTimeField(default=timezone.now)


class PredictionMaison(models.Model):
    adresse_numero = models.CharField(max_length=10, default='')
    adresse_suffixe = models.CharField(max_length=2, choices=SUFFIXE_CHOICES, blank=True, null=True, default='')
    adresse_code_voie = models.CharField(max_length=100, choices=TYPES_VOIE_CHOICES, default='')
    adresse_nom_voie = models.CharField(max_length=100, default='')
    code_postal = models.CharField(max_length=10)
    ville = models.CharField(max_length=100, blank=True)
    region = models.CharField(max_length=100, choices=REGIONS_CHOICES, default='')
    departement = models.CharField(max_length=100)
    superficie = models.FloatField()
    nombre_de_pieces = models.IntegerField()
    superficie_terrain = models.FloatField()
    prix_estime = models.FloatField()
    date_predicted = models.DateTimeField(default=timezone.now)


class Transformer:
    data: pd.DataFrame
    X: pd.DataFrame
    y: pd.Series

    def fit(self, data):
        self.data = pd.DataFrame()
        column = 'date-mutation'

        df = pd.to_datetime(data[column], format='%Y-%m-%d')
        self.data['year'] = df.dt.year
        self.data['month'] = df.dt.month
        self.data['day'] = df.dt.day

        column = 'no-voie'
        self.data[column] = data[column].astype('Int64')

        column = 'b/t/q'
        self.data[column] = data[column].astype('category')

        column = 'type-de-voie'
        self.data[column] = data[column].astype('category')

        column = 'voie'
        self.data[column] = data[column].astype('category')
        # TODO: in the next step we will
        # convert the address to a coordinate
        # two columns: latitude and longitude
        column = 'code-postal'
        self.data[column] = data[column].astype('Int64')

        column = 'type-local'
        self.data[column] = data[column].astype('category')

        column = 'surface-terrain'
        self.data[column] = data[column]

        column = 'surface-reelle-bati'
        self.data[column] = data[column]

        column = 'nombre-pieces-principales'
        self.data[column] = data[column].astype('Int64')

        # Let it here.
        self.X = self.data.copy()
        for column in self.X.columns:
            if self.X[column].dtype.name == 'category':
                self.X[column] = self.X[column].cat.codes
        self.y = data['valeur-fonciere']

        return self

    def transform(self, data):
        X = pd.DataFrame()

        column = 'date-mutation'
        df = pd.to_datetime(data[column], format='%Y-%m-%d')
        X['year'] = df.dt.year
        X['month'] = df.dt.month
        X['day'] = df.dt.day

        column = 'no-voie'
        X[column] = data[column].astype('Int64')

        column = 'b/t/q'
        X[column] = data[column].apply(
            lambda x: self.data[column].cat.categories.get_loc(x) if x in self.data[column].cat.categories else -1
        )

        column = 'type-de-voie'
        X[column] = data[column].apply(
            lambda x: self.data[column].cat.categories.get_loc(x) if x in self.data[column].cat.categories else -1
        )

        column = 'voie'
        X[column] = data[column].apply(
            lambda x: self.data[column].cat.categories.get_loc(x) if x in self.data[column].cat.categories else -1
        )

        column = 'code-postal'
        X[column] = data[column].astype('Int64')

        column = 'type-local'
        X[column] = data[column].apply(
            lambda x: self.data[column].cat.categories.get_loc(x) if x in self.data[column].cat.categories else -1
        )

        column = 'surface-terrain'
        X[column] = data[column]

        column = 'surface-reelle-bati'
        X[column] = data[column]

        column = 'nombre-pieces-principales'
        X[column] = data[column].astype('Int64')

        return X

    def save(self, path):
        self.data.to_csv(path, index=False)


def load_transformer(path: str) -> Transformer:
    transformer = Transformer()
    data = pd.read_csv(path)
    transformer.data = data

    columns = [
        'b/t/q',
        'type-de-voie',
        'voie',
        'type-local'
    ]
    for column in columns:
        transformer.data[column] = transformer.data[column].astype('category')

    columns = [
        'no-voie',
        'code-postal',
        'nombre-pieces-principales'
    ]
    for column in columns:
        transformer.data[column] = transformer.data[column].astype('Int64')

    return transformer