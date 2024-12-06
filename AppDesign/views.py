from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .forms import RegisterUserForm
from .models import AdvUser
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView

def index(request):
    return render(request, 'catalog/index.html')

@login_required
def profile(request):
    return render(request, 'catalog/profile.html')

class login(LoginView):
    template_name = 'catalog/login.html'

class logout(LoginRequiredMixin, LogoutView):
    template_name = 'catalog/logout.html'

class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'catalog/register_user.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('catalog:register_done')

class RegisterDoneView(TemplateView):
    template_name = 'catalog/register_done.html'
