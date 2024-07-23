from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import AppartementForm, MaisonForm
from . import prediction
from .models import PredictionAppart, PredictionMaison
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
avg_file_path = os.path.join(BASE_DIR, 'average_prices_by_departement.json')

def creer_appartement(request):
    if request.method == 'POST':
        form = AppartementForm(request.POST)
        if form.is_valid():
            adresse_numero = form.cleaned_data['adresse_numero']
            adresse_suffixe = form.cleaned_data['adresse_suffixe']
            adresse_code_voie = form.cleaned_data['adresse_code_voie']
            adresse_nom_voie = form.cleaned_data['adresse_nom_voie']
            region = form.cleaned_data['region']
            departement = form.cleaned_data['departement']
            ville = form.cleaned_data['ville']
            code_postal = form.cleaned_data['code_postal']
            superficie = form.cleaned_data['superficie']
            nombre_de_pieces = form.cleaned_data['nombre_de_pieces']
            etage = form.cleaned_data['etage']
            ascenseur = form.cleaned_data['ascenseur']

            prix_estime = prediction.predict_price_appartement(adresse_numero, adresse_suffixe, adresse_code_voie, adresse_nom_voie, region, code_postal, superficie, nombre_de_pieces, etage, ascenseur)
            prix_estime = int(prix_estime)
            prix_m2 = prix_estime / superficie

            prediction_appart = PredictionAppart.objects.create(
                adresse_numero=adresse_numero,
                adresse_suffixe=adresse_suffixe,
                adresse_code_voie=adresse_code_voie,
                adresse_nom_voie=adresse_nom_voie,
                region=region,
                departement=departement,
                ville=ville,
                code_postal=code_postal,
                superficie=superficie,
                nombre_de_pieces=nombre_de_pieces,
                etage=etage,
                ascenseur=ascenseur,
                prix_estime=prix_estime
            )
            print(adresse_code_voie)
            return redirect('prediction_result', prediction_type='appartement', prediction_id=prediction_appart.id)
        else:
            # Debug message
            print("Formulaire non valide")
            print(form.errors)
    else:
        form = AppartementForm()

    return render(request, 'creer_appartement.html', {'form': form})

def creer_maison(request):
    if request.method == 'POST':
        form = MaisonForm(request.POST)
        if form.is_valid():
            adresse_numero = form.cleaned_data['adresse_numero']
            adresse_suffixe = form.cleaned_data['adresse_suffixe']
            adresse_code_voie = form.cleaned_data['adresse_code_voie']
            adresse_nom_voie = form.cleaned_data['adresse_nom_voie']
            region = form.cleaned_data['region']
            departement = form.cleaned_data['departement']
            ville = form.cleaned_data['ville']
            code_postal = form.cleaned_data['code_postal']
            superficie = form.cleaned_data['superficie']
            superficie_terrain = form.cleaned_data['superficie_terrain']
            nombre_de_pieces = form.cleaned_data['nombre_de_pieces']

            prix_estime = prediction.predict_price_maison(adresse_numero, adresse_suffixe, adresse_code_voie, adresse_nom_voie, region, code_postal, superficie, superficie_terrain, nombre_de_pieces)
            prix_estime = int(prix_estime)
            prix_m2 = prix_estime / superficie

            prediction_maison  = PredictionMaison.objects.create(
                adresse_numero=adresse_numero,
                adresse_suffixe=adresse_suffixe,
                adresse_code_voie=adresse_code_voie,
                adresse_nom_voie=adresse_nom_voie,
                code_postal=code_postal,
                region=region,
                departement=departement,
                ville=ville,
                superficie=superficie,
                superficie_terrain=superficie_terrain,
                nombre_de_pieces=nombre_de_pieces,
                prix_estime=prix_estime
            )

            return redirect('prediction_result', prediction_type='maison', prediction_id=prediction_maison.id)
        else:
            # Debug message
            print("Formulaire non valide")
            print(form.errors)
    else:
        form = MaisonForm()

    return render(request, 'creer_maison.html', {'form': form})


def prediction_result(request, prediction_type, prediction_id):
    if prediction_type == 'appartement':
        prediction = PredictionAppart.objects.get(id=prediction_id)
    elif prediction_type == 'maison':
        prediction = PredictionMaison.objects.get(id=prediction_id)
    else:
        prediction = None

    if prediction:
        prix_m2 = prediction.prix_estime / prediction.superficie
    else:
        prix_m2 = None

    return render(request, 'prediction_result.html', {'prediction': prediction, 'type': prediction_type, 'prix_m2': prix_m2})

def get_estimates(request):
    departement = request.GET.get('departement')
    if not departement:
        return JsonResponse({'error': 'Missing departement parameter'}, status=400)
    
    try:
        with open(avg_file_path, 'r', encoding='utf-8') as json_file:
            average_prices = json.load(json_file)

        data = average_prices.get(departement, {})
        if not data:
            return JsonResponse({'error': 'No data found for this departement'}, status=404)

        response_data = {
            'appartement': {
                'moyenne': data.get('appartement', {}).get('average_price', 'N/A'),
                'moyenne_sqm': data.get('appartement', {}).get('average_price_per_sqm', 'N/A')
            },
            'maison': {
                'moyenne': data.get('maison', {}).get('average_price', 'N/A'),
                'moyenne_sqm': data.get('maison', {}).get('average_price_per_sqm', 'N/A')
            }
        }
        return JsonResponse(response_data)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def home(request):
    predictions_appart = PredictionAppart.objects.all().order_by('-date_predicted')[:10]
    predictions_maison = PredictionMaison.objects.all().order_by('-date_predicted')[:10]
    with open(avg_file_path, 'r', encoding='utf-8') as json_file:
        average_prices = json.load(json_file)
    return render(request, 'home.html', {
        'predictions_appart': predictions_appart,
        'predictions_maison': predictions_maison,
        'average_prices': json.dumps(average_prices)
    })
