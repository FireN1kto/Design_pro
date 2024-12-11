from django.urls import path
from .views import index, login, profile, logout, RegisterDoneView, RegisterUserView, create_request, delete_request

app_name = 'AppDesign'

urlpatterns = [
    path('accounts/profile/', profile, name='profile'),
    path('', index, name='index'),
    path('accounts/login/', login.as_view(), name='login'),
    path('accounts/logout/', logout.as_view(), name='logout'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('create-request', create_request, name='create_requests'),
    path('delete-request/', delete_request, name='delete_request'),
]
