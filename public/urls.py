from django.urls import path, include

from . import views

app_name = 'public'
urlpatterns = [
    path('', views.index, name='index'),
    path('contribute/', views.contribute, name='contribute'),
    path('contribution/<int:route_id>/', views.contribution, name='contribution'),
    path('nodes/', views.get_map_relevant_nodes, name='nodes'),
    path('accounts/', include('accounts.urls')),
]
