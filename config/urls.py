from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('text_analyzer.urls')),
]
