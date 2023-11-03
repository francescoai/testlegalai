# mio_progetto/urls.py

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chat_openai.urls')),  # Includi le rotte di chat_openai alla radice
    # Aggiungi altre rotte del progetto qui sotto, se necessario
]
