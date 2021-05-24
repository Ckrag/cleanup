from django.urls import path

from . import views

app_name = 'public'
urlpatterns = [
    path('', views.index, name='index'),
    path('contribution', views.contribution, name='contribution'),
    path('nodes', views.get_map_relevant_nodes, name='nodes')
]
