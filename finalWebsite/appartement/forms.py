from django import forms
from .models import PredictionAppart, PredictionMaison, REGIONS_CHOICES, TYPES_VOIE_CHOICES, SUFFIXE_CHOICES
from django.utils import timezone


class AppartementForm(forms.ModelForm):
    nombre_de_pieces = forms.IntegerField(initial=0)
    etage = forms.IntegerField(initial=0)
    region = forms.ChoiceField(choices=REGIONS_CHOICES, label="Région")
    departement = forms.CharField(label="Département", max_length=100)
    adresse_suffixe = forms.ChoiceField(choices=SUFFIXE_CHOICES, label='Suffixe d\'adresse', required=False, initial='')
    adresse_code_voie = forms.ChoiceField(choices=TYPES_VOIE_CHOICES, label='Type de voie')

    class Meta:
        model = PredictionAppart
        fields = ['adresse_numero', 'adresse_suffixe', 'adresse_code_voie', 'adresse_nom_voie', 'code_postal', 'ville', 'region', 'departement', 'superficie', 'nombre_de_pieces', 'etage', 'ascenseur']
        widgets = {
            'region': forms.Select(choices=REGIONS_CHOICES),
            'adresse_suffixe': forms.Select(choices=SUFFIXE_CHOICES),
            'adresse_code_voie': forms.Select(choices=TYPES_VOIE_CHOICES),
        }

class MaisonForm(forms.ModelForm):
    nombre_de_pieces = forms.IntegerField(initial=0)
    region = forms.ChoiceField(choices=REGIONS_CHOICES, label="Région", initial='')
    departement = forms.CharField(label="Département", max_length=100)
    adresse_suffixe = forms.ChoiceField(choices=SUFFIXE_CHOICES, label='Suffixe d\'adresse', required=False, initial='')
    adresse_code_voie = forms.ChoiceField(choices=TYPES_VOIE_CHOICES, label='Type de voie', initial='')

    class Meta:
        model = PredictionMaison
        fields = ['adresse_numero', 'adresse_suffixe', 'adresse_code_voie', 'adresse_nom_voie', 'code_postal', 'ville', 'region', 'departement', 'superficie', 'nombre_de_pieces', 'superficie_terrain']
        widgets = {
            'region': forms.Select(choices=REGIONS_CHOICES),
            'adresse_suffixe': forms.Select(choices=SUFFIXE_CHOICES),
            'adresse_code_voie': forms.Select(choices=TYPES_VOIE_CHOICES),
        }