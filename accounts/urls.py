from django.urls import path, include

from . import views
from .views import SignUpView

app_name = ''
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('signup/', SignUpView.as_view(), name='signup'),
]
