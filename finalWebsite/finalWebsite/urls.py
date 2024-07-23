from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('appartement.urls')),  # Inclure les URLs de l'application 'appartement'
]
