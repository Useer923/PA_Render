from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('creer_appartement/', views.creer_appartement, name='creer_appartement'),
    path('creer_maison/', views.creer_maison, name='creer_maison'),
    path('prediction_result/<str:prediction_type>/<int:prediction_id>/', views.prediction_result, name='prediction_result'),
    path('get_estimates/', views.get_estimates, name='get_estimates'),

]
