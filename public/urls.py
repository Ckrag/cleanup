from django.urls import path

from . import views

app_name = 'public'
urlpatterns = [
    path('', views.index, name='index'),
    path('contribution', views.contribution, name='contribution'),
    path('create_contribution', views.create_contribution, name='create contribution'),
]
