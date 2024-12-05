from django.urls import path
from .views import index

app_name = 'AppDesign'

urlpatterns = [
    path('', index, name='index'),
]
