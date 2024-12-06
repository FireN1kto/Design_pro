from django.urls import path
from .views import index, login, profile, logout, RegisterDoneView, RegisterUserView, activate_user

app_name = 'AppDesign'

urlpatterns = [
    path('accounts/profile/', profile, name='profile'),
    path('', index, name='index'),
    path('accounts/login/', login.as_view(), name='login'),
    path('accounts/logout/', logout.as_view(), name='logout'),
    path('accounts/register/done/', RegisterDoneView.as_view(), name='register_done'),
    path('accounts/register/', RegisterUserView.as_view(), name='register'),
    path('accounts/register/activate/', activate_user, name='activate'),
]
