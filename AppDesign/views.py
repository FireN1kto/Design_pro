from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .forms import RegisterUserForm
from .models import AdvUser
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login

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

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.is_activated = False
        user.has_logged_in = False
        user.save()

        messages.success(self.request, 'Вы успешно зарегистрированы! Ожидайте активации от администратора.')

        return super().form_valid(form)

class RegisterDoneView(TemplateView):
    template_name = 'catalog/register_done.html'

def activate_user(request, user_id):
    user = get_object_or_404(AdvUser, id=user_id)
    user.is_activated = True
    user.is_active = True
    user.save()
    messages.success(request, f'Пользователь {user.username} успешно активирован!')
    return redirect('admin:index')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            auth_login(request, user)
            user.has_logged_in = True
            user.save()
            return redirect('catalog/index')  # Перенаправление на главную страницу или другую страницу

    return render(request, 'login.html')  # Ваш шаблон для входа