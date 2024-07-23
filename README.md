Pour run l'application, lancer :

python .\finalWebsite\manage.py runserver


Commande pour supprimer l'historique des estimations sur la Homepage :

'''
python .\finalWebsite\manage.py shell 
PredictionAppart.objects.all().delete()
PredictionMaison.objects.all().delete()
exit()
'''